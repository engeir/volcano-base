"""Load the Otto-Bliesner et al. 2016 data into xarray objects."""

import datetime
import re
from typing import Literal, overload

import numpy as np
import scipy
import xarray as xr

import volcano_base


def _get_ob16_rf_temp_arrays() -> tuple[list[xr.DataArray], list[xr.DataArray]]:
    """Create samples from Otto-Bliesner et al. 2016.

    Returns
    -------
    tuple[list[xr.DataArray], list[xr.DataArray]]
        The RF and temperature arrays in two lists

    Raises
    ------
    FileNotFoundError
        If the directory where all the files is not found.
    """
    # Need AOD and RF seasonal and annual means, as well as an array of equal length
    # with the corresponding time-after-eruption.
    path = volcano_base.config.DATA_PATH / "cesm-lme"
    if not path.exists():
        raise FileNotFoundError(
            "Cannot find CESM-LME files. You may try to run the `save_to_npz` function"
            f" within {__name__}."
        )
    pattern = re.compile("([A-Z]+)-00[1-5]\\.npz$", re.X)
    files_ = list(path.rglob("*00[1-5].npz"))
    rf, temp = [], []
    for file in files_:
        if isinstance(search := pattern.search(str(file)), re.Match):
            array = _load_numpy(file.resolve())
            s = "0850-01-01"
            t = xr.cftime_range(
                start=s, periods=len(array.data), calendar="noleap", freq="D"
            )
            if search.groups()[0] == "TREFHT":
                temp.append(array.assign_coords({"time": t}))
            elif search.groups()[0] == "FSNTOA":
                rf.append(array.assign_coords({"time": t}))
    return rf, temp


def _load_numpy(np_file) -> xr.DataArray:
    """Load the content of an npz file as an xarray DataArray."""
    with np.load(np_file, allow_pickle=True) as data:
        two_dim_data = 2
        if data["data"].ndim == two_dim_data:
            if "lev" in data.files and data["lev"].shape != ():
                lev_str = "lev"
            elif "ilev" in data.files and data["ilev"].shape != ():
                lev_str = "ilev"
            else:
                raise KeyError(f"There is no level information in the file {np_file}")
            coords = {"time": data["times"], lev_str: data[lev_str]}
            dims = ["time", lev_str]
        else:
            coords = {"time": data["times"]}
            dims = ["time"]
        xarr = xr.DataArray(data["data"], dims=dims, coords=coords)
    return xarr


def _remove_seasonality_ob16(arr: xr.DataArray, monthly: bool = False) -> xr.DataArray:
    """Remove seasonality by subtracting CESM LME control run."""
    file_name = (
        volcano_base.config.DATA_PATH / "cesm-lme" / "TREFHT850forcing-control-003.npz"
    )
    if file_name.exists():
        array = _load_numpy(file_name.resolve())
        s = "0850-01-01"
        t = xr.cftime_range(
            start=s, periods=len(array.data), calendar="noleap", freq="D"
        )
        raw_temp = array.assign_coords({"time": t})
    if monthly:
        raw_temp = raw_temp.resample(time="MS").mean()
        raw_temp, arr = xr.align(raw_temp, arr)
        month_mean = raw_temp.groupby("time.month").mean("time")
        return (
            arr.groupby("time.month") - month_mean + volcano_base.config.MEANS["TREFHT"]
        )
    day_mean = raw_temp.groupby("time.dayofyear").mean()
    raw_temp, arr = xr.align(raw_temp, arr)
    return (
        arr.groupby("time.dayofyear") - day_mean + volcano_base.config.MEANS["TREFHT"]
    )


@overload
def get_ob16_rf(ensemble: Literal[False] = False) -> xr.DataArray:
    ...


@overload
def get_ob16_rf(ensemble: Literal[True]) -> list[xr.DataArray]:
    ...


def get_ob16_rf(ensemble: bool = False) -> xr.DataArray | list[xr.DataArray]:
    """Return Otto-Bliesner et al. 2016 radiative forcing.

    Parameters
    ----------
    ensemble : bool, optional
        Whether to return the full ensemble or just the median, by default False

    Returns
    -------
    xr.DataArray | list[xr.DataArray]
        The radiative forcing time series
    """
    rf, _ = _get_ob16_rf_temp_arrays()
    if ensemble:
        return rf
    # Add RF from the FSNTOA variable (daily) ---------------------------------------- #
    # We load in the original FSNTOA 5 member ensemble and compute the ensemble mean.
    rf_fr = volcano_base.manipulate.get_median(rf, xarray=True)
    # Remove noise in Fourier domain (seasonal and 6-month cycles)
    rf_fr = volcano_base.manipulate.remove_seasonality([rf_fr.copy()])[0]
    rf_fr = volcano_base.manipulate.remove_seasonality([rf_fr], freq=2)[0]
    # Subtract the mean
    rf_fr.data -= rf_fr.data.mean()
    return rf_fr


@overload
def get_ob16_temperature(ensemble: Literal[False] = False) -> xr.DataArray:
    ...


@overload
def get_ob16_temperature(ensemble: Literal[True]) -> list[xr.DataArray]:
    ...


def get_ob16_temperature(ensemble: bool = False) -> xr.DataArray | list[xr.DataArray]:
    """Return Otto-Bliesner et al. 2016 temperature.

    Parameters
    ----------
    ensemble : bool, optional
        Whether to return the full ensemble or just the median, by default False

    Returns
    -------
    xr.DataArray | list[xr.DataArray]
        The temperature time series
    """
    # Temperature
    _, temp_ = _get_ob16_rf_temp_arrays()
    if ensemble:
        return temp_
    temp_xr = volcano_base.manipulate.get_median(temp_, xarray=True)
    # Seasonality is removed by use of a control run temperature time series, where we
    # compute a climatology mean for each day of the year which is subtracted from the
    # time series.
    # temp_xr = temp_xr.assign_coords(time=volcano_base.manipulate.float2dt(temp_xr.time.data))
    temp_xr = _remove_seasonality_ob16(temp_xr)
    # Adjust the temperature so its mean is at zero. We also remove a slight drift by
    # means of a linear regression fit.
    x_ax = volcano_base.manipulate.dt2float(temp_xr.time.data)
    temp_lin_reg = scipy.stats.linregress(x_ax, temp_xr.data)
    temp_xr.data -= x_ax * temp_lin_reg.slope + temp_lin_reg.intercept
    return temp_xr


def get_ob16_outputs(
    only_peaks: bool = True,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return Otto-Bliesner et al. 2016 SO2, RF and temperature peaks.

    The peaks are best estimates from the full time series.

    Parameters
    ----------
    only_peaks : bool, optional
        Whether to return only the peaks or the full time series, by default True.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        SO2 peaks, RF peaks and temperature peaks
    """
    # Set fluctuations to be positive
    temp_xr = get_ob16_temperature()
    temp_xr.data *= -1
    rf_fr = get_ob16_rf()
    rf_fr.data *= -1

    # Scale forcing from SO4 to SO2
    so2_start = volcano_base.load.get_so2_ob16_peak_timeseries(xarray=True) / 3 * 2
    # A 210 days shift forward give the best timing of the temperature peak and 150
    # days forward give the timing for the radiative forcing peak. A 190 days shift
    # back give the best timing for when the temperature and radiative forcing
    # perturbations start (eruption day). Done by eye measure.
    d1, d2, d3 = 190, 150, 210
    so2_start = so2_start.assign_coords(
        time=so2_start.time.data - datetime.timedelta(days=d1)
    )
    so2_rf_peak = so2_start.assign_coords(
        time=so2_start.time.data + datetime.timedelta(days=d2)
    )
    so2_temp_peak = so2_start.assign_coords(
        time=so2_start.time.data + datetime.timedelta(days=d3)
    )

    so2_start, so2_rf_peak, so2_temp_peak, rf_fr, temp = xr.align(
        so2_start, so2_rf_peak, so2_temp_peak, rf_fr, temp_xr
    )

    if not len(so2_start) % 2:
        so2_start = so2_start[:-1]
        so2_rf_peak = so2_rf_peak[:-1]
        so2_temp_peak = so2_rf_peak[:-1]
        rf_fr = rf_fr[:-1]
        temp = temp[:-1]
    _cesm_lme_so2_start = so2_start
    _cesm_lme_so2_rf_peak = so2_rf_peak
    _cesm_lme_so2_temp_peak = so2_temp_peak
    _cesm_lme_rf = rf_fr
    _cesm_lme_temp = temp
    if not only_peaks:
        return _cesm_lme_so2_start.data, rf_fr.data, temp.data
    # Mask out all non-zero forcing values, and the corresponding temperature values.
    _idx_rf = np.argwhere(so2_rf_peak.data > 0)
    _idx_temp = np.argwhere(so2_temp_peak.data > 0)
    so2 = so2_rf_peak.data[_idx_rf].flatten()
    rf_v = rf_fr.data[_idx_rf].flatten()
    temp_v = temp.data[_idx_temp].flatten()
    _ids = so2.argsort()
    return so2[_ids], rf_v[_ids], temp_v[_ids]


if __name__ == "__main__":
    _get_ob16_rf_temp_arrays()
