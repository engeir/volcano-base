"""Load the Otto-Bliesner et al. 2016 data into xarray objects."""

# FIXME: need to fix the day/month issue, think the raw FSNTOA just need to be ironed
# out and put in npz files. After that the class should be more or less done.

import datetime
import itertools
import pathlib
import re
from collections import deque
from typing import Literal, Never, NoReturn

import matplotlib.pyplot as plt
import nc_time_axis  # noqa: F401
import numpy as np
import scipy
import xarray as xr
from pydantic import BaseModel, Field

import volcano_base


def _never_called(value: Never) -> NoReturn:
    """Return nothing only when the input does not exist."""
    # The function is useful when running mypy. If, in a series of if/elif or
    # match/case, a variable is not fully handled, mypy will complain and say that the
    # variable is of the wrong type when this function is called in the final `else`
    # clause.
    raise AssertionError("Code is unreachable.")


class OttoBliesner(BaseModel):
    """Object holding time series related to data from Otto-Bliesner et al. (2016)."""

    freq: Literal["h0", "h1"] = Field(
        default="h1",
        frozen=True,
        description="Frequency of data as set by the nhtfrq field (https://www2.cesm.ucar.edu/models/cesm1.0/cesm/cesm_doc_1_0_4/x2602.html)",
    )
    _temperature_ensemble: tuple[
        xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray
    ] | None = None
    _rf_ensemble: tuple[
        xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray
    ] | None = None
    _temperature_median: xr.DataArray | None = None
    _rf_median: xr.DataArray | None = None
    _temperature_peaks: np.ndarray | None = None
    _rf_peaks: np.ndarray | None = None
    _so2: xr.DataArray | None = None
    _so2_delta: xr.DataArray | None = None
    _aligned_arrays: dict[
        Literal["so2-start", "so2-rf", "so2-temperature", "rf", "temperature"],
        xr.DataArray,
    ] | None = None
    _so2_peaks: np.ndarray | None = None

    class Config:
        """Configuration for the OttoBliesner BaseModel object."""

        validate_assignment = True

    @property
    def temperature_ensemble(
        self,
    ) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]:
        """Return the temperature ensemble."""
        _calls = 0
        while self._temperature_ensemble is None:
            if _calls > 1:
                raise ValueError("Could not set temperature ensemble.")
            self.temperature_ensemble = self._set_rf_temp_ensembles("TREFHT")
            _calls += 1
        return self._temperature_ensemble

    @temperature_ensemble.setter
    def temperature_ensemble(
        self,
        value: tuple[
            xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray
        ],
    ) -> None:
        """Set the temperature ensemble."""
        self._temperature_ensemble = value

    @property
    def rf_ensemble(
        self,
    ) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]:
        """Return the radiative forcing ensemble."""
        _calls = 0
        while self._rf_ensemble is None:
            if _calls > 1:
                raise ValueError("Could not set RF ensemble.")
            self.rf_ensemble = self._set_rf_temp_ensembles("FSNTOA")
            _calls += 1
        return self._rf_ensemble

    @rf_ensemble.setter
    def rf_ensemble(
        self,
        value: tuple[
            xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray
        ],
    ) -> None:
        """Set the radiative forcing ensemble."""
        self._rf_ensemble = value

    @property
    def rf_median(self) -> xr.DataArray:
        """Return the median of the radiative forcing time series."""
        _calls = 0
        while self._rf_median is None:
            if _calls > 1:
                raise ValueError("Could not set RF median.")
            self._set_rf_median()
            _calls += 1
        return self._rf_median

    @rf_median.setter
    def rf_median(self, value: xr.DataArray) -> None:
        """Set the median of the radiative forcing time series."""
        self._rf_median = value

    @property
    def temperature_median(self) -> xr.DataArray:
        """Return the median of the temperature time series."""
        _calls = 0
        while self._temperature_median is None:
            if _calls > 1:
                raise ValueError("Could not set temperature median.")
            self._set_temperature_median()
            _calls += 1
        return self._temperature_median

    @temperature_median.setter
    def temperature_median(self, value: xr.DataArray) -> None:
        """Set the median of the temperature time series."""
        self._temperature_median = value

    @property
    def temperature_peaks(self) -> np.ndarray:
        """Return the temperature peaks."""
        _calls = 0
        while self._temperature_peaks is None:
            if _calls > 1:
                raise ValueError("Could not set temperature peaks.")
            self._set_peak_arrays()
            _calls += 1
        return self._temperature_peaks

    @temperature_peaks.setter
    def temperature_peaks(self, value: np.ndarray) -> None:
        """Set the temperature peaks."""
        self._temperature_peaks = value

    @property
    def rf_peaks(self) -> np.ndarray:
        """Return the radiative forcing peaks."""
        _calls = 0
        while self._rf_peaks is None:
            if _calls > 1:
                raise ValueError("Could not set RF peaks.")
            self._set_peak_arrays()
            _calls += 1
        return self._rf_peaks

    @rf_peaks.setter
    def rf_peaks(self, value: np.ndarray) -> None:
        """Set the radiative forcing peaks."""
        self._rf_peaks = value

    @property
    def so2(self) -> xr.DataArray:
        """Return the SO2 time series."""
        _calls = 0
        while self._so2 is None:
            if _calls > 1:
                raise ValueError("Could not set SO2 time series.")
            self._set_so2_full_timeseries()
            _calls += 1
        return self._so2

    @so2.setter
    def so2(self, value: xr.DataArray) -> None:
        """Set the SO2 time series."""
        self._so2 = value

    @property
    def so2_delta(self) -> xr.DataArray:
        """Return the SO2 delta time series."""
        _calls = 0
        while self._so2_delta is None:
            if _calls > 1:
                raise ValueError("Could not set SO2 delta time series.")
            self._set_so2_peak_timeseries()
            _calls += 1
        return self._so2_delta

    @so2_delta.setter
    def so2_delta(self, value: xr.DataArray) -> None:
        """Set the SO2 delta time series."""
        self._so2_delta = value

    @property
    def aligned_arrays(
        self,
    ) -> dict[
        Literal["so2-start", "so2-rf", "so2-temperature", "rf", "temperature"],
        xr.DataArray,
    ]:
        """Return RF and temperature arrays with SO2 arrays aligned to their start and peak."""
        _calls = 0
        while self._aligned_arrays is None:
            if _calls > 1:
                raise ValueError("Could not set aligned arrays.")
            self._set_aligned_arrays()
            _calls += 1
        return self._aligned_arrays

    @aligned_arrays.setter
    def aligned_arrays(
        self,
        value: dict[
            Literal["so2-start", "so2-rf", "so2-temperature", "rf", "temperature"],
            xr.DataArray,
        ],
    ) -> None:
        """Set the aligned arrays."""
        self._aligned_arrays = value

    @property
    def so2_peaks(self) -> np.ndarray:
        """Return the SO2 peaks."""
        _calls = 0
        while self._so2_peaks is None:
            if _calls > 1:
                raise ValueError("Could not set SO2 peaks.")
            self._set_peak_arrays()
            _calls += 1
        return self._so2_peaks

    @so2_peaks.setter
    def so2_peaks(self, value: np.ndarray) -> None:
        """Set the SO2 peaks."""
        self._so2_peaks = value

    def _set_so2_full_timeseries(self) -> None:
        """Load the npz file with volcanic injection."""
        file = "IVI2LoadingLatHeight501-2000_L18_c20100518.nc"
        # file = "IVI2LoadingLatHeight501-2000_L18_c20121018_KT.nc"
        if not (fn := volcano_base.config.DATA_PATH / "cesm-lme" / file).exists():
            print(f"Cannot find {fn.resolve()}")
            volcano_base.down.save_historical_so2(fn)
        ds = xr.open_dataset(fn)
        avgs_list = volcano_base.manipulate.mean_flatten([ds.colmass], dims=["lat"])
        avgs = avgs_list[0]
        # Scale so that the unit is now in Tg(SO2) (Otto-Bliesner et al. (2016)).
        avgs = avgs / avgs.max() * 257.9 / 3 * 2
        f_time = avgs.time.data
        f_time = f_time - f_time[0] + 501
        avgs = avgs.assign_coords(
            time=volcano_base.manipulate.float2dt(f_time, freq="MS")
        )
        self.so2 = avgs

    def _set_so2_peak_timeseries(self) -> None:
        """Load in mean stratospheric volcanic sulfate aerosol injections.

        The time series are daily resolved, with SO2 injections represented as single day
        peaks.

        Notes
        -----
        The data is from Gao et al. (2008) `data
        <http://climate.envsci.rutgers.edu/IVI2/>`_, and was used as input to the model
        simulations by Otto-Bliesner et al. (2016).
        """
        time_ = volcano_base.manipulate.dt2float(self.so2.time.data)
        so2 = self.so2.data
        so2, time_ = self._find_peaks_in_so2(so2, time_)
        match self.freq:
            case "h0":
                freq = "MS"
            case "h1":
                freq = "D"
            case _:
                _never_called(self.freq)
        da = xr.DataArray(
            so2,
            dims=["time"],
            coords={"time": volcano_base.manipulate.float2dt(time_, freq)},
            name="Mean stratospheric volcanic sulfate aerosol injections [Tg]",
        )
        da = da.assign_coords(time=da.time.data + datetime.timedelta(days=14))
        self.so2_delta = da

    def _find_peaks_in_so2(
        self,
        frc: np.ndarray,
        time_: xr.CFTimeIndex,
    ) -> tuple[np.ndarray, xr.CFTimeIndex]:
        new_frc = np.zeros_like(frc)
        limit = 2e-6
        for i, v in enumerate(frc):
            if i == 0 and v > limit:
                new_frc[i] = v
                continue
            if v > limit and v > frc[i - 1]:
                new_frc[i] = v
            if new_frc[i - 1] > limit and new_frc[i - 1] < v:
                new_frc[i - 1] = 0
        # Go from monthly to daily (this is fine as long as we use a spiky forcing). We
        # start in December.
        match self.freq:
            case "h0":
                ...
            case "h1":
                new_frc = self._month2day(new_frc, start=12)
                # The new time axis now goes down to one day
                thetime_ = np.linspace(501, 2002, (2002 - 501) * 365 + 1)
                thetime_ = thetime_[: len(new_frc)]
                time_ = xr.CFTimeIndex(thetime_)
            case _:
                _never_called(self.freq)
        return new_frc, time_

    @staticmethod
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

    def _set_rf_temp_ensembles(
        self, search_group: str
    ) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]:
        """Create samples from Otto-Bliesner et al. 2016.

        Parameters
        ----------
        search_group : str
            The variable to search for in the files.

        Returns
        -------
        tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]
            The ensemble members.

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
        match self.freq:
            case "h1":
                pattern = re.compile("/([A-Z]+)-00[1-5]\\.npz$", re.X)
            case "h0":
                pattern = re.compile("/([A-Z]+)-monthly-00[1-5]\\.npz$", re.X)
            case _:
                _never_called(self.freq)
        files_ = list(path.rglob("*00[1-5].npz"))
        return self._load_npz(files_, pattern, search_group)

    def _load_npz(
        self, files_: list[pathlib.Path], pattern: re.Pattern, search_group: str
    ) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]:
        maxfiles = 5
        arrs: deque[xr.DataArray] = deque([], maxlen=maxfiles)
        for file in files_:
            if isinstance(search := pattern.search(str(file)), re.Match):
                if search.groups()[0] == search_group:
                    print(file.resolve())
                    print(search.groups())
                    array = self._load_numpy(file.resolve())
                    s = "0850-01-01"
                    t = xr.cftime_range(
                        start=s, periods=len(array.data), calendar="noleap", freq="D"
                    )
                    arrs.append(array.assign_coords({"time": t}))
        if len(arrs) != maxfiles:
            raise ValueError(
                "The number of ensemble members is not 5. Please check the files."
            )
        return arrs[0], arrs[1], arrs[2], arrs[3], arrs[4]

    def _load_nc(
        self, files_: list[pathlib.Path], pattern: re.Pattern, search_group: str
    ) -> list[xr.DataArray]:
        arrs = []
        for file in files_:
            if isinstance(search := pattern.search(str(file)), re.Match):
                print(search.groups())
                print(file.resolve())
                array = xr.open_dataset(file.resolve())
                if search.groups()[0] == search_group:
                    arrs.append(array[search_group])
        return arrs

    @staticmethod
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
                    raise KeyError(
                        f"There is no level information in the file {np_file}"
                    )
                coords = {"time": data["times"], lev_str: data[lev_str]}
                dims = ["time", lev_str]
            else:
                coords = {"time": data["times"]}
                dims = ["time"]
            xarr = xr.DataArray(data["data"], dims=dims, coords=coords)
        return xarr

    def _remove_temp_seasonality(self, arr: xr.DataArray) -> xr.DataArray:
        """Remove seasonality by subtracting CESM LME control run."""
        file_name = (
            volcano_base.config.DATA_PATH
            / "cesm-lme"
            / "TREFHT850forcing-control-003.npz"
        )
        if file_name.exists():
            array = self._load_numpy(file_name.resolve())
            s = "0850-01-01"
            t = xr.cftime_range(
                start=s, periods=len(array.data), calendar="noleap", freq="D"
            )
            raw_temp = array.assign_coords({"time": t})
        match self.freq:
            case "h0":
                raw_temp = raw_temp.resample(time="MS").mean()
                raw_temp, arr = xr.align(raw_temp, arr)
                month_mean = raw_temp.groupby("time.month").mean("time")
                return (
                    arr.groupby("time.month")
                    - month_mean
                    + volcano_base.config.MEANS["TREFHT"]
                )
            case "h1":
                day_mean = raw_temp.groupby("time.dayofyear").mean()
                raw_temp, arr = xr.align(raw_temp, arr)
                return (
                    arr.groupby("time.dayofyear")
                    - day_mean
                    + volcano_base.config.MEANS["TREFHT"]
                )
            case _:
                _never_called(self.freq)

    def _set_rf_median(self) -> None:
        """Return Otto-Bliesner et al. 2016 radiative forcing."""
        rf = volcano_base.manipulate.get_median(
            list(self.rf_ensemble).copy(), xarray=True
        )
        # Remove noise in Fourier domain (seasonal and 6-month cycles)
        rf = volcano_base.manipulate.remove_seasonality([rf.copy()])[0]
        rf = volcano_base.manipulate.remove_seasonality([rf], freq=2)[0]
        # Subtract the mean
        rf.data -= rf.data.mean()
        self.rf_median = rf

    def _set_temperature_median(self) -> None:
        """Return Otto-Bliesner et al. 2016 temperature."""
        temp = volcano_base.manipulate.get_median(
            list(self.temperature_ensemble).copy(), xarray=True
        )
        # Seasonality is removed by use of a control run temperature time series, where we
        # compute a climatology mean for each day of the year which is subtracted from the
        # time series.
        temp = self._remove_temp_seasonality(temp)
        # Adjust the temperature so its mean is at zero. We also remove a slight drift by
        # means of a linear regression fit.
        x_ax = volcano_base.manipulate.dt2float(temp.time.data)
        temp_lin_reg = scipy.stats.linregress(x_ax, temp.data)
        temp.data -= x_ax * temp_lin_reg.slope + temp_lin_reg.intercept
        self.temperature_median = temp

    def _set_aligned_arrays(self) -> None:
        """Return Otto-Bliesner et al. 2016 SO2, RF and temperature peaks.

        The peaks are best estimates from the full time series.
        """
        # Set fluctuations to be positive
        temp = self.temperature_median
        temp.data *= -1
        rf = self.rf_median
        rf.data *= -1

        so2_start = self.so2_delta
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

        so2_start, so2_rf_peak, so2_temp_peak, rf, temp = xr.align(
            so2_start, so2_rf_peak, so2_temp_peak, rf, temp
        )

        if not len(so2_start) % 2:
            so2_start = so2_start[:-1]
            so2_rf_peak = so2_rf_peak[:-1]
            so2_temp_peak = so2_rf_peak[:-1]
            rf = rf[:-1]
            temp = temp[:-1]
        self.aligned_arrays = {
            "so2-start": so2_start,
            "so2-rf": so2_rf_peak,
            "so2-temperature": so2_temp_peak,
            "rf": rf,
            "temperature": temp,
        }

    def _set_peak_arrays(self) -> None:
        # Mask out all non-zero SO2 values, and the corresponding RF and temperature
        # values.
        _idx_rf = np.argwhere(self.aligned_arrays["so2-rf"].data > 0)
        _idx_temp = np.argwhere(self.aligned_arrays["so2-temperature"].data > 0)
        so2 = self.aligned_arrays["so2-rf"].data[_idx_rf].flatten()
        rf_v = self.aligned_arrays["rf"].data[_idx_rf].flatten()
        temp_v = self.aligned_arrays["temperature"].data[_idx_temp].flatten()
        _ids = so2.argsort()
        self.so2_peaks = so2[_ids]
        self.rf_peaks = rf_v[_ids]
        self.temperature_peaks = temp_v[_ids]


def main():
    """Run the main function."""
    ob16_day = OttoBliesner()
    plt.plot(ob16_day.so2_peaks, ob16_day.rf_peaks)
    plt.plot(ob16_day.so2_peaks, ob16_day.temperature_peaks)
    plt.figure()
    ob16_day.aligned_arrays["rf"].plot()
    ob16_day.aligned_arrays["temperature"].plot()
    ob16_day.aligned_arrays["so2-start"].plot()
    ob16_day.aligned_arrays["so2-rf"].plot()
    ob16_day.aligned_arrays["so2-temperature"].plot()
    plt.show()


if __name__ == "__main__":
    main()
