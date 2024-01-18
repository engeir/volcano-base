"""Load historic data from the CESM LME simulations."""

import datetime
import itertools
from typing import Literal, overload

import numpy as np
import xarray as xr

import volcano_base


def get_so2_ob16_full_timeseries() -> tuple[np.ndarray, np.ndarray]:
    """Load the npz file with volcanic injection.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Arrays containing time and value of SO2 peaks
    """
    file = "IVI2LoadingLatHeight501-2000_L18_c20100518.nc"
    if not (fn := volcano_base.config.DATA_PATH / "cesm-lme" / file).exists():
        print(f"Cannot find {fn.resolve()}")
        volcano_base.down.save_historical_so2(fn)
    ds = xr.open_dataset(fn)
    year = ds.time.data
    avgs_list = volcano_base.manipulate.mean_flatten([ds.colmass], dims=["lat"])
    avgs = avgs_list[0].data
    # Scale so that the unit is now in Tg (Otto-Bliesner et al. (2016)).
    avgs = avgs / avgs.max() * 257.9
    return year, avgs


def _gao_remove_decay_in_forcing(
    frc: np.ndarray, y: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    new_frc = np.zeros_like(frc)
    limit = 2e-6
    place_here = 1
    for i, v in enumerate(frc[1:]):
        if frc[i - 1] < v and v > limit and frc[i - 1] < limit:
            new_frc[i + place_here] = v
        if new_frc[i + place_here - 1] > limit and v > new_frc[i + place_here - 1]:
            new_frc[i + place_here - 1] = 0
            new_frc[i + place_here] = v
    # Go from monthly to daily (this is fine as long as we use a spiky forcing). We
    # start in December.
    new_frc = _month2day(new_frc, start=12)
    # The new time axis now goes down to one day
    y = np.linspace(501, 2002, (2002 - 501) * 365 + 1)
    y = y[: len(new_frc)]
    return new_frc, y


def _month2day(
    arr: np.ndarray,
    start: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] = 1,
) -> np.ndarray:
    # Go from monthly to daily
    newest = np.array([])
    # Add 30, 29 or 27 elements between all elements: months -> days
    days_ = (30, 27, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30)
    days = itertools.cycle(days_)
    for _ in range(start - 1):
        next(days)
    for month in arr:
        insert_ = np.zeros(next(days))
        newest = np.r_[newest, np.array([month])]
        newest = np.r_[newest, insert_]
    # The new time axis now goes down to one day
    return newest


@overload
def get_so2_ob16_peak_timeseries(
    xarray: Literal[False],
) -> tuple[np.ndarray, np.ndarray]:
    ...


@overload
def get_so2_ob16_peak_timeseries(xarray: Literal[True]) -> xr.DataArray:
    ...


def get_so2_ob16_peak_timeseries(
    xarray: bool = False,
) -> tuple[np.ndarray, np.ndarray] | xr.DataArray:
    """Load in mean stratospheric volcanic sulfate aerosol injections.

    The time series are daily resolved, with SO2 injections represented as single day
    peaks.

    Parameters
    ----------
    xarray : bool, optional
        Whether to return the data as an xarray DataArray or to use the default of two
        numpy arrays. Default is False

    Returns
    -------
    tuple[np.ndarray, np.ndarray] | xr.DataArray
        The stratospheric sulfate injections used as forcing in the CESM LME
        simulations. Arrival times are in the first array, SO2 values in the second.

    Notes
    -----
    The data is from Gao et al. (2008) `data
    <http://climate.envsci.rutgers.edu/IVI2/>`_, and was used as input to the model
    simulations by Otto-Bliesner et al. (2017).
    """
    y, g = get_so2_ob16_full_timeseries()
    # plt.figure()
    # plt.plot(y, g)
    y = y - y[0] + 501
    g, y = _gao_remove_decay_in_forcing(g, y)
    # plt.plot(y, g)
    # plt.show()
    if xarray:
        freq = "D"
        da = xr.DataArray(
            g,
            dims=["time"],
            coords={"time": volcano_base.manipulate.float2dt(y, freq)},
            name="Mean stratospheric volcanic sulfate aerosol injections [Tg]",
        )
        da = da.assign_coords(time=da.time.data + datetime.timedelta(days=14))
        return da
    return y, g
