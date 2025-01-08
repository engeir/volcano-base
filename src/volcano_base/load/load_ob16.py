"""Load the Otto-Bliesner et al. 2016 data into xarray objects."""

import datetime
import itertools
import os
import pathlib
import re
import warnings
from typing import Literal

import nc_time_axis  # noqa: F401
import numpy as np
import rich.progress
import scipy
import xarray as xr
from numpy.typing import NDArray
from pydantic import BaseModel, Field

import volcano_base


class Ob16FileNotFound(FileNotFoundError):
    """Raise an error if one of the Otto-Bliesner et al. (2016) files are not found."""

    def __init__(self, *args: str) -> None:
        if args:
            msg = f'Cannot find the file "{args[0]}", which is a necessary Otto-Blienser et al. (2016) file.'
        else:
            msg = "Cannot find the necessary Otto-Bliesner et al. (2016) files."
        self.message = f"{msg} Please run the `save_to_npz` function within `down.ob16` to see what files are missing."
        super().__init__(self.message)


class OttoBliesner(BaseModel):  # noqa: PLR0904
    """Object holding time series related to data from Otto-Bliesner et al. (2016).

    Attributes
    ----------
    freq : Literal["h0", "h1"], optional
        Frequency of data as set by the nhtfrq field
        (https://www2.cesm.ucar.edu/models/cesm1.0/cesm/cesm_doc_1_0_4/x2602.html), by
        default "h1".
    progress : bool, optional
        Show progress bar while loading in data. By default False.
    """

    freq: Literal["h0", "h1"] = Field(
        default="h1",
        description="Frequency of data as set by the nhtfrq field (https://www2.cesm.ucar.edu/models/cesm1.0/cesm/cesm_doc_1_0_4/x2602.html)",
    )
    progress: bool = Field(
        default=False, description="Show progress bar while loading in data."
    )
    _temperature_ensemble: tuple[
        xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray
    ]
    _temperature_median: xr.DataArray
    _temperature_control_raw: xr.DataArray
    _temperature_control: xr.DataArray
    _temperature_peaks: NDArray[np.float64]
    _surfacetemp_ensemble: tuple[
        xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray
    ]
    _surfacetemp_median: xr.DataArray
    _surfacetemp_control_raw: xr.DataArray
    _surfacetemp_control: xr.DataArray
    _surfacetemp_peaks: NDArray[np.float64]
    _rf_ensemble: tuple[
        xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray
    ]
    _rf_median: xr.DataArray
    _rf_control_raw: xr.DataArray
    _rf_control: xr.DataArray
    _rf_peaks: NDArray[np.float64]
    _icefrac_ensemble: tuple[
        xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray
    ]
    _icefrac_median: xr.DataArray
    _icefrac_control_raw: xr.DataArray
    _icefrac_control: xr.DataArray
    _icefrac_peaks: NDArray[np.float64]
    _so2: xr.DataArray
    _so2_delta: xr.DataArray
    _aligned_arrays: dict[
        Literal[
            "so2-decay-start",
            "so2-start",
            "so2-rf",
            "so2-temperature",
            "icefrac",
            "rf",
            "surfacetemp",
            "temperature",
        ],
        xr.DataArray,
    ]
    _so2_peaks: NDArray[np.float64]

    class Config:
        """Configuration for the OttoBliesner BaseModel object."""

        validate_assignment = True
        frozen = True
        extra = "forbid"
        strict = True

    @property
    def temperature_ensemble(
        self,
    ) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]:
        """Return the temperature ensemble.

        Returns
        -------
        tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]
            The ensemble members.
        """
        if not hasattr(self, "_temperature_ensemble"):
            self._temperature_ensemble = self._set_variable_ensembles("TREFHT")
        return self._temperature_ensemble

    @property
    def temperature_median(self) -> xr.DataArray:
        """Return the median of the temperature time series.

        Returns
        -------
        xr.DataArray
            Median of the temperature time series
        """
        if not hasattr(self, "_temperature_median"):
            self._set_temperature_median()
        return self._temperature_median

    @property
    def temperature_control_raw(self) -> xr.DataArray:
        """Return the raw control temperature time series.

        Returns
        -------
        xr.DataArray
            The control temperature time series
        """
        if not hasattr(self, "_temperature_control_raw"):
            self._set_temperature_median()
        return self._temperature_control_raw

    @property
    def temperature_control(self) -> xr.DataArray:
        """Return the control temperature time series.

        Returns
        -------
        xr.DataArray
            The control temperature time series
        """
        if not hasattr(self, "_temperature_control"):
            self._set_temperature_median()
        return self._temperature_control

    @property
    def temperature_peaks(self) -> NDArray[np.float64]:
        """Return the temperature peaks.

        Returns
        -------
        NDArray[np.float64]
            Array holding all found peak values
        """
        if not hasattr(self, "_temperature_peaks"):
            self._set_peak_arrays()
        return self._temperature_peaks

    @property
    def surfacetemp_ensemble(
        self,
    ) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]:
        """Return the sea-ice fractions ensemble.

        Returns
        -------
        tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]
            The ensemble members.
        """
        if not hasattr(self, "_surfacetemp_ensemble"):
            self._surfacetemp_ensemble = self._set_variable_ensembles("TS")
        return self._surfacetemp_ensemble

    @property
    def surfacetemp_median(self) -> xr.DataArray:
        """Return the median of the sea-ice fraction time series.

        Returns
        -------
        xr.DataArray
            Median of the sea-ice fraction time series
        """
        self._set_surfacetemp_median()
        return self._surfacetemp_median

    @property
    def surfacetemp_control_raw(self) -> xr.DataArray:
        """Return the raw control TS time series.

        Returns
        -------
        xr.DataArray
            The control TS time series
        """
        if not hasattr(self, "_surfacetemp_control_raw"):
            self._set_surfacetemp_median()
        return self._surfacetemp_control_raw

    @property
    def surfacetemp_control(self) -> xr.DataArray:
        """Return the control TS time series.

        Returns
        -------
        xr.DataArray
            The control TS time series
        """
        if not hasattr(self, "_surfacetemp_control"):
            self._set_surfacetemp_median()
        return self._surfacetemp_control

    @property
    def surfacetemp_peaks(self) -> NDArray[np.float64]:
        """Return the sea-ice fraction peaks.

        Returns
        -------
        NDArray[np.float64]
            Array holding all found peak values
        """
        if not hasattr(self, "_surfacetemp_peaks"):
            self._set_peak_arrays()
        return self._surfacetemp_peaks

    @property
    def rf_ensemble(
        self,
    ) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]:
        """Return the radiative forcing ensemble.

        Returns
        -------
        tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]
            The ensemble members.
        """
        if not hasattr(self, "_rf_ensemble"):
            self._rf_ensemble = self._set_variable_ensembles("FSNTOA")
        return self._rf_ensemble

    @property
    def rf_median(self) -> xr.DataArray:
        """Return the median of the radiative forcing time series.

        Returns
        -------
        xr.DataArray
            Median of the radiative forcing time series
        """
        self._set_rf_median()
        return self._rf_median

    @property
    def rf_control_raw(self) -> xr.DataArray:
        """Return the raw control RF time series.

        Returns
        -------
        xr.DataArray
            The control RF time series
        """
        if not hasattr(self, "_rf_control_raw"):
            self._set_rf_median()
        return self._rf_control_raw

    @property
    def rf_control(self) -> xr.DataArray:
        """Return the control RF time series.

        Returns
        -------
        xr.DataArray
            The control RF time series
        """
        if not hasattr(self, "_rf_control"):
            self._set_rf_median()
        return self._rf_control

    @property
    def rf_peaks(self) -> NDArray[np.float64]:
        """Return the radiative forcing peaks.

        Returns
        -------
        NDArray[np.float64]
            Array holding all found peak values
        """
        if not hasattr(self, "_rf_peaks"):
            self._set_peak_arrays()
        return self._rf_peaks

    @property
    def icefrac_ensemble(
        self,
    ) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]:
        """Return the sea-ice fractions ensemble.

        Returns
        -------
        tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]
            The ensemble members.
        """
        if not hasattr(self, "_icefrac_ensemble"):
            self._icefrac_ensemble = self._set_variable_ensembles("ICEFRAC")
        return self._icefrac_ensemble

    @property
    def icefrac_median(self) -> xr.DataArray:
        """Return the median of the sea-ice fraction time series.

        Returns
        -------
        xr.DataArray
            Median of the sea-ice fraction time series
        """
        self._set_icefrac_median()
        return self._icefrac_median

    @property
    def icefrac_control_raw(self) -> xr.DataArray:
        """Return the raw control ICEFRAC time series.

        Returns
        -------
        xr.DataArray
            The control ICEFRAC time series
        """
        if not hasattr(self, "_icefrac_control_raw"):
            self._set_icefrac_median()
        return self._icefrac_control_raw

    @property
    def icefrac_control(self) -> xr.DataArray:
        """Return the control ICEFRAC time series.

        Returns
        -------
        xr.DataArray
            The control ICEFRAC time series
        """
        if not hasattr(self, "_icefrac_control"):
            self._set_icefrac_median()
        return self._icefrac_control

    @property
    def icefrac_peaks(self) -> NDArray[np.float64]:
        """Return the sea-ice fraction peaks.

        Returns
        -------
        NDArray[np.float64]
            Array holding all found peak values
        """
        if not hasattr(self, "_icefrac_peaks"):
            self._set_peak_arrays()
        return self._icefrac_peaks

    @property
    def so2(self) -> xr.DataArray:
        """Return the SO2 time series.

        Returns
        -------
        xr.DataArray
            The original SO2 time series
        """
        if not hasattr(self, "_so2"):
            self._set_so2_full_timeseries()
        return self._so2

    @property
    def so2_delta(self) -> xr.DataArray:
        """Return the SO2 delta time series.

        Returns
        -------
        xr.DataArray
            The SO2 time series with peaks only
        """
        if not hasattr(self, "_so2_delta"):
            self._set_so2_peak_timeseries()
        return self._so2_delta

    @property
    def aligned_arrays(
        self,
    ) -> dict[
        Literal[
            "so2-decay-start",
            "so2-start",
            "so2-rf",
            "so2-temperature",
            "icefrac",
            "rf",
            "surfacetemp",
            "temperature",
        ],
        xr.DataArray,
    ]:
        """Return the aligned SO2, RF and temperature arrays.

        Returns
        -------
        dict[Literal['so2-decay-start', 'so2-start', 'so2-rf', 'so2-temperature', 'icefrac', 'rf', 'surfacetemp', 'temperature'], xr.DataArray]
            The RF and temperature arrays along with SO2 arrays aligned with the
            eruption start, RF peak and temperature peak.
        """
        if not hasattr(self, "_aligned_arrays"):
            self._set_aligned_arrays()
        return self._aligned_arrays

    @property
    def so2_peaks(self) -> NDArray[np.float64]:
        """Return the SO2 peaks.

        Returns
        -------
        NDArray[np.float64]
            Array holding all SO2 peak values
        """
        self._set_peak_arrays()
        return self._so2_peaks

    def _set_so2_full_timeseries(self) -> None:
        """Load the npz file with volcanic injection."""
        file = "IVI2LoadingLatHeight501-2000_L18_c20100518.nc"
        if not (fn := volcano_base.config.DATA_PATH / "cesm-lme" / file).exists():
            print(f"Cannot find {fn.resolve()}")
            volcano_base.down.save_historical_so2(fn)
        ds = xr.open_dataset(fn)
        avgs_list = volcano_base.manipulate.mean_flatten([ds.colmass], dims=["lat"])
        avgs = avgs_list[0]
        # Scale so that the unit is now in Tg(SO2) (Otto-Bliesner et al. (2016)).
        avgs *= 510e3  # From kg/m2 to Tg/Earth surface
        f_time = avgs.time.data
        f_time = f_time - f_time[0] + 501
        avgs = avgs.assign_coords(
            time=volcano_base.manipulate.float2dt(f_time, freq="MS")
            + datetime.timedelta(days=14)
        )
        self._so2 = avgs

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
                volcano_base.never_called(self.freq)
        da = xr.DataArray(
            so2,
            dims=["time"],
            coords={"time": volcano_base.manipulate.float2dt(time_, freq)},
            name="Mean stratospheric volcanic sulfate aerosol injections [Tg]",
        )
        da = da.assign_coords(time=da.time.data + datetime.timedelta(days=14))
        self._so2_delta = da

    def _find_peaks_in_so2(
        self,
        frc: NDArray[np.float64],
        time_: xr.CFTimeIndex,
    ) -> tuple[NDArray[np.float64], xr.CFTimeIndex]:
        new_array = np.zeros_like(frc)
        limit = 2e-6
        for i, v in enumerate(frc):
            if i == 0 and v > limit:
                new_array[i] = v
                continue
            if v > limit and v > frc[i - 1]:
                new_array[i] = v
            if new_array[i - 1] > limit and new_array[i - 1] < v:
                new_array[i - 1] = 0
        # Go from monthly to daily (this is fine as long as we use a spiky forcing). We
        # start in December.
        match self.freq:
            case "h0":
                ...
            case "h1":
                new_array = self._month2day(new_array, start=12)
                time_ = self._so2_daily_time_axis(new_array)
            case _:
                volcano_base.never_called(self.freq)
        return new_array, time_

    def _month2day(
        self,
        arr: NDArray[np.float64],
        start: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] = 1,
        multiplier: int | Literal["auto"] = 0,
    ) -> NDArray[np.float64]:
        # Go from monthly to daily
        newest = np.array([])
        # Add 30, 29 or 27 elements between all elements: months -> days
        days_ = (30, 27, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30)
        days = itertools.cycle(days_)
        for _ in range(start - 1):
            next(days)
        progress = self._setup_progress_bar()
        with progress:
            task_add_days = progress.add_task(
                "[cyan]Converting from monthly to daily resolution...",
                total=len(arr),
                start=False,
            )
            if self.progress:
                progress.start_task(task_add_days)
            else:
                progress.stop()
            for month in arr:
                mult = float(month) if multiplier == "auto" else multiplier
                insert_ = np.ones(next(days)) * mult
                newest = np.r_[newest, np.array([month])]
                newest = np.r_[newest, insert_]
                if self.progress:
                    progress.advance(task_add_days)
            if self.progress:
                progress.stop_task(task_add_days)
        # The new time axis now goes down to one day
        return newest

    def _set_variable_ensembles(
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
        Ob16FileNotFound
            If the directory with all the files is not found.
        """
        # Need AOD and RF seasonal and annual means, as well as an array of equal length
        # with the corresponding time-after-eruption.
        path: pathlib.Path = volcano_base.config.DATA_PATH / "cesm-lme"
        if not path.exists():
            raise Ob16FileNotFound(str(path.resolve()))
        match self.freq:
            case "h1":
                pattern = re.compile("/([A-Z]+)-00[1-5]\\.npz$", re.X)
            case "h0":
                pattern = re.compile("/([A-Z]+)-monthly-00[1-5]\\.npz$", re.X)
            case _:
                volcano_base.never_called(self.freq)
        files_ = list(path.rglob("*00[1-5].npz"))
        return self._load_npz(files_, pattern, search_group)

    @staticmethod
    def _setup_progress_bar() -> rich.progress.Progress:
        return rich.progress.Progress(
            rich.progress.TextColumn("[progress.description]{task.description}"),
            rich.progress.SpinnerColumn(),
            rich.progress.BarColumn(),
            rich.progress.TaskProgressColumn(),
            rich.progress.MofNCompleteColumn(),
            rich.progress.TimeRemainingColumn(elapsed_when_finished=True),
            transient=True,
        )

    def _load_npz(
        self, files_: list[pathlib.Path], pattern: re.Pattern, search_group: str
    ) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]:
        arrs: list[xr.DataArray] = []
        maxfiles = 5
        match self.freq:
            case "h1":
                freq = "D"
                shift = 0
            case "h0":
                freq = "MS"
                shift = 15
            case _:
                volcano_base.never_called(self.freq)
        progress = self._setup_progress_bar()
        with progress:
            task_find_files = progress.add_task(
                f"[cyan]Loading {search_group} files...",
                total=maxfiles,
                start=False,
            )
            if self.progress:
                progress.start_task(task_find_files)
            else:
                progress.stop()
            for file in files_:
                if isinstance(search := pattern.search(str(file)), re.Match):
                    if search.groups()[0] == search_group:
                        array = self._load_numpy(file.resolve())
                        s = "0850-01-01"
                        t = xr.cftime_range(
                            start=s,
                            periods=len(array.data),
                            calendar="noleap",
                            freq=freq,
                        ) + datetime.timedelta(days=shift)
                        arrs.append(array.assign_coords({"time": t}))
                        if self.progress:
                            progress.advance(task_find_files)
            if self.progress:
                progress.stop_task(task_find_files)
        if len(arrs) != maxfiles:
            raise Ob16FileNotFound()
        return arrs[0], arrs[1], arrs[2], arrs[3], arrs[4]

    @staticmethod
    def _load_nc(
        files_: list[pathlib.Path], pattern: re.Pattern, search_group: str
    ) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray]:
        arrs: list[xr.DataArray] = []
        for file in files_:
            if isinstance(search := pattern.search(str(file)), re.Match):
                array = xr.open_dataset(file.resolve())
                if search.groups()[0] == search_group:
                    arrs.append(array[search_group])
        maxfiles = 5
        if len(arrs) != maxfiles:
            raise ValueError(
                f"The number of ensemble members is not 5, found {len(arrs)}. Please check the files."
            )
        return arrs[0], arrs[1], arrs[2], arrs[3], arrs[4]

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

    def _subtract_climatology(
        self,
        variable: Literal["ICEFRAC", "TREFHT", "FSNTOA", "TS"],
        raw_arr: xr.DataArray,
        arr: xr.DataArray,
        groupby: Literal["time.dayofyear", "time.month"],
    ) -> xr.DataArray:
        """Subtract the climatological mean.

        Parameters
        ----------
        variable : Literal["ICEFRAC", "TREFHT", "FSNTOA", "TS"]
            The variable to subtract the climatology from.
        raw_arr : xr.DataArray
            The raw data array to take the climatology from.
        arr : xr.DataArray
            The data array to subtract the climatology from.
        groupby : Literal["time.dayofyear", "time.month"]
            The groupby string to use when grouping the data.

        Returns
        -------
        xr.DataArray
            The data array with the climatology subtracted.
        """
        raw_arr, arr = xr.align(raw_arr, arr)
        climatology_ = raw_arr.groupby(groupby)
        climatology = (
            climatology_.mean("time") if "month" in groupby else climatology_.mean()
        )
        if variable == "TREFHT":
            self._temperature_control_raw = raw_arr
            self._temperature_control = raw_arr.groupby(groupby) - climatology
        elif variable == "TS":
            self._surfacetemp_control_raw = raw_arr
            self._surfacetemp_control = raw_arr.groupby(groupby) - climatology
        elif variable == "FSNTOA":
            self._rf_control_raw = raw_arr
            self._rf_control = raw_arr.groupby(groupby) - climatology
        elif variable == "ICEFRAC":
            self._icefrac_control_raw = raw_arr
            self._icefrac_control = raw_arr.groupby(groupby) - climatology
        return arr.groupby(groupby) - climatology

    def _remove_temp_seasonality(self, arr: xr.DataArray) -> xr.DataArray:
        """Remove seasonality by subtracting CESM LME control run."""
        match self.freq:
            case "h0":
                f1 = "MS"
                specifier = "-monthly"
                shift = 15
            case "h1":
                f1 = "D"
                specifier = ""
                shift = 0
            case _:
                volcano_base.never_called(self.freq)
        file_name = (
            volcano_base.config.DATA_PATH
            / "cesm-lme"
            / f"TREFHT850forcing-control{specifier}-003.npz"
        )
        raw_temp = self._load_into_xarray(file_name, f1, shift)
        match self.freq:
            case "h0":
                return (
                    self._subtract_climatology("TREFHT", raw_temp, arr, "time.month")
                    + volcano_base.config.MEANS["TREFHT"]
                )
            case "h1":
                return (
                    self._subtract_climatology(
                        "TREFHT", raw_temp, arr, "time.dayofyear"
                    )
                    + volcano_base.config.MEANS["TREFHT"]
                )
            case _:
                volcano_base.never_called(self.freq)

    def _remove_attr_seasonality_ctrl(
        self, arr: xr.DataArray, name: Literal["ICEFRAC", "FSNTOA", "TS"]
    ) -> xr.DataArray:
        """Remove seasonality by subtracting CESM LME control run."""
        match self.freq:
            case "h0":
                f1 = "MS"
                specifier = "-monthly"
                shift = 15
            case "h1":
                f1 = "D"
                specifier = ""
                shift = 0
            case _:
                volcano_base.never_called(self.freq)
        file_name = (
            volcano_base.config.DATA_PATH
            / "cesm-lme"
            / f"{name}850forcing-control{specifier}-003.npz"
        )
        raw_arr = self._load_into_xarray(file_name, f1, shift)
        match self.freq:
            case "h0":
                return self._subtract_climatology(name, raw_arr, arr, "time.month")
            case "h1":
                return self._subtract_climatology(name, raw_arr, arr, "time.dayofyear")
            case _:
                volcano_base.never_called(self.freq)

    def _load_into_xarray(
        self, file_name: pathlib.Path, f1: str, shift: int
    ) -> xr.DataArray:
        if not file_name.exists():
            raise Ob16FileNotFound(str(file_name.resolve()))
        array = self._load_numpy(file_name.resolve())
        s = "0850-01-01"
        t = xr.cftime_range(
            start=s, periods=len(array.data), calendar="noleap", freq=f1
        ) + datetime.timedelta(days=shift)
        return array.assign_coords({"time": t})

    def _remove_attr_seasonality(
        self, attr: xr.DataArray, name: Literal["FSNTOA", "ICEFRAC", "TS"]
    ) -> xr.DataArray:
        strategy_ctrl = True
        if not strategy_ctrl:
            # Remove noise in Fourier domain (seasonal and 6-month cycles)
            match self.freq:
                case "h0":
                    f1 = 1.014
                case "h1":
                    f1 = 1
                case _:
                    volcano_base.never_called(self.freq)
            attr = volcano_base.manipulate.remove_seasonality([attr.copy()], freq=f1)[0]
            attr = volcano_base.manipulate.remove_seasonality([attr], freq=f1 * 2)[0]
        else:
            attr = self._remove_attr_seasonality_ctrl(attr, name)
        return attr

    def _set_icefrac_median(self) -> None:
        """Return Otto-Bliesner et al. 2016 sea-ice fractions."""
        icefrac = volcano_base.manipulate.get_median(
            list(self.icefrac_ensemble).copy(), xarray=True
        )
        icefrac = self._remove_attr_seasonality(icefrac, "ICEFRAC")
        # Adjust the sea-ice fraction so its mean is at zero. We also remove a slight
        # drift by means of a linear regression fit.
        x_ax = volcano_base.manipulate.dt2float(icefrac.time.data)
        icefrac_lin_reg = scipy.stats.linregress(x_ax, icefrac.data)
        icefrac.data -= x_ax * icefrac_lin_reg.slope + icefrac_lin_reg.intercept
        self._icefrac_median = icefrac

    def _set_rf_median(self) -> None:
        """Return Otto-Bliesner et al. 2016 radiative forcing."""
        rf = volcano_base.manipulate.get_median(
            list(self.rf_ensemble).copy(), xarray=True
        )
        rf = self._remove_attr_seasonality(rf, "FSNTOA")
        # Subtract the mean
        rf.data -= rf.data.mean()
        self._rf_median = rf

    def _set_surfacetemp_median(self) -> None:
        """Return Otto-Bliesner et al. 2016 surface temperatures."""
        surfacetemp = volcano_base.manipulate.get_median(
            list(self.surfacetemp_ensemble).copy(), xarray=True
        )
        surfacetemp = self._remove_attr_seasonality(surfacetemp, "TS")
        # Subtract the mean
        surfacetemp.data -= surfacetemp.data.mean()
        self._surfacetemp_median = surfacetemp

    def _set_temperature_median(self) -> None:
        """Return Otto-Bliesner et al. 2016 temperature."""
        temp = volcano_base.manipulate.get_median(
            list(self.temperature_ensemble).copy(), xarray=True
        )
        # Seasonality is removed by use of a control run temperature time series, where
        # we compute a climatology mean for each day of the year which is subtracted
        # from the time series.
        temp = self._remove_temp_seasonality(temp)
        # Adjust the temperature so its mean is at zero. We also remove a slight drift
        # by means of a linear regression fit.
        x_ax = volcano_base.manipulate.dt2float(temp.time.data)
        temp_lin_reg = scipy.stats.linregress(x_ax, temp.data)
        temp.data -= x_ax * temp_lin_reg.slope + temp_lin_reg.intercept
        self._temperature_median = temp

    def _force_align(  # noqa: PLR0913, PLR0917
        self,
        so2_decay_start: xr.DataArray,
        so2_start: xr.DataArray,
        icefrac: xr.DataArray,
        rf: xr.DataArray,
        surfacetemp: xr.DataArray,
        temp: xr.DataArray,
    ) -> tuple[
        xr.DataArray,
        xr.DataArray,
        xr.DataArray,
        xr.DataArray,
        xr.DataArray,
        xr.DataArray,
        xr.DataArray,
        xr.DataArray,
    ]:
        # A 44 days shift forward give the best timing of the temperature peak and 31
        # days backward give the timing for the radiative forcing peak. A 180 days shift
        # back give the best timing for when the temperature and radiative forcing
        # perturbations start (eruption day). The original (daily, expanded with
        # step-functions) SO2 input is shifted back 58 days. Done by eye measure.
        match self.freq:
            case "h1":
                new_array = self._month2day(
                    so2_decay_start.data, start=12, multiplier="auto"
                )
                time_ = self._so2_daily_time_axis(new_array)
                so2_decay_start = xr.DataArray(
                    new_array,
                    dims=["time"],
                    coords={"time": volcano_base.manipulate.float2dt(time_, "D")},
                    name="Mean stratospheric volcanic sulfate aerosol injections [Tg]",
                )
                so2_decay_start = so2_decay_start.assign_coords(
                    time=so2_decay_start.time.data + datetime.timedelta(days=14)
                )
                d1, d2, d3, d4 = 180, -31, 44, 58
                # We hard-code the slices to avoid the time consuming `xr.align` process
                slices = (
                    slice(127429, -122),  # `sds_slice`
                    slice(127551, None),  # `ss_slice`
                    slice(127402, -149),  # `sr_slice`
                    slice(127327, -224),  # `st_slice`
                    slice(0, -1929),  # `rf_slice`
                    slice(0, -1929),  # `temp_slice`
                )
                so2_rf_peak = so2_start.assign_coords(
                    time=so2_start.time.data + datetime.timedelta(days=d2)
                )
                so2_temp_peak = so2_start.assign_coords(
                    time=so2_start.time.data + datetime.timedelta(days=d3)
                )
                so2_decay_start = so2_decay_start.assign_coords(
                    time=so2_decay_start.time.data - datetime.timedelta(days=d4)
                )
                so2_start = so2_start.assign_coords(
                    time=so2_start.time.data - datetime.timedelta(days=d1)
                )
            case "h0":
                d1, d2, d3, d4 = 15, 15, 15, 15
                slices = (
                    slice(4190, -4),  # `sds_slice`
                    slice(4194, None),  # `ss_slice`
                    slice(4189, -5),  # `sr_slice`
                    slice(4184, -10),  # `st_slice`
                    slice(None, -64),  # `rf_slice`
                    slice(None, -64),  # `temp_slice`
                )
                so2_rf_peak = so2_start.assign_coords(
                    time=xr.cftime_range(
                        "0500-12", "2010", freq="MS", calendar="noleap"
                    )[: len(so2_start)]
                    + datetime.timedelta(days=d2)
                )
                so2_temp_peak = so2_start.assign_coords(
                    time=xr.cftime_range(
                        "0501-05", "2010", freq="MS", calendar="noleap"
                    )[: len(so2_start)]
                    + datetime.timedelta(days=d3)
                )
                so2_decay_start = so2_decay_start.assign_coords(
                    time=xr.cftime_range(
                        "0500-11", "2010", freq="MS", calendar="noleap"
                    )[: len(so2_start)]
                    + datetime.timedelta(days=d4)
                )
                so2_start = so2_start.assign_coords(
                    time=xr.cftime_range(
                        "0500-07", "2010", freq="MS", calendar="noleap"
                    )[: len(so2_start)]
                    + datetime.timedelta(days=d1)
                )
            case _:
                volcano_base.never_called(self.freq)

        # Aligning the arrays takes a long time, so since we know the exact indices we
        # instead slice the arrays to the correct length. Basically zero time versus 15
        # seconds.
        # so2_decay_start, so2_start, so2_rf_peak, so2_temp_peak, rf, temp = xr.align(
        #     so2_decay_start, so2_start, so2_rf_peak, so2_temp_peak, rf, temp
        # )
        so2_decay_start = so2_decay_start[slices[0]]
        so2_start = so2_start[slices[1]]
        so2_rf_peak = so2_rf_peak[slices[2]]
        so2_temp_peak = so2_temp_peak[slices[3]]
        icefrac = icefrac[slices[4]]
        rf = rf[slices[4]]
        surfacetemp = surfacetemp[slices[4]]
        temp = temp[slices[5]]
        return (
            so2_decay_start,
            so2_start,
            so2_rf_peak,
            so2_temp_peak,
            icefrac,
            rf,
            surfacetemp,
            temp,
        )

    def _set_aligned_arrays(self) -> None:
        """Return Otto-Bliesner et al. 2016 SO2, RF and temperature peaks.

        The peaks are best estimates from the full time series.
        """
        # Set fluctuations to be positive
        temp = self.temperature_median.copy()
        temp.data *= -1
        surfacetemp = self.surfacetemp_median.copy()
        surfacetemp.data *= -1
        rf = self.rf_median.copy()
        rf.data *= -1
        icefrac = self.icefrac_median.copy()

        (
            so2_decay_start,
            so2_start,
            so2_rf_peak,
            so2_temp_peak,
            icefrac,
            rf,
            surfacetemp,
            temp,
        ) = self._force_align(
            self.so2.copy(), self.so2_delta.copy(), icefrac, rf, surfacetemp, temp
        )

        if not len(so2_start) % 2:
            so2_decay_start = so2_decay_start[:-1]
            so2_start = so2_start[:-1]
            so2_rf_peak = so2_rf_peak[:-1]
            so2_temp_peak = so2_temp_peak[:-1]
            icefrac = icefrac[:-1]
            rf = rf[:-1]
            surfacetemp = surfacetemp[:-1]
            temp = temp[:-1]
        self._aligned_arrays = {
            "so2-decay-start": so2_decay_start,
            "so2-start": so2_start,
            "so2-rf": so2_rf_peak,
            "so2-temperature": so2_temp_peak,
            "icefrac": icefrac,
            "rf": rf,
            "surfacetemp": surfacetemp,
            "temperature": temp,
        }

    @staticmethod
    def _so2_daily_time_axis(array: NDArray[np.float64]) -> xr.CFTimeIndex:
        time_ = xr.cftime_range(start="0501", end="2002", freq="D", calendar="noleap")[
            : len(array)
        ]
        days_in_year = 365
        time_ = time_.map(lambda x: x.toordinal() / days_in_year)
        return time_

    def _set_peak_arrays(self) -> None:
        if self.freq == "h0":
            _warn_skips = (os.path.dirname(__file__),)
            warnings.warn(  # noqa: B028
                "The peak finding is more precise when working with daily data."
                " If you are interested in finding peak values of RF and"
                " temperature, use daily frequency (`h1`).",
                skip_file_prefixes=_warn_skips,
            )
        # Mask out all non-zero SO2 values, and the corresponding RF and temperature
        # values.
        _idx_rf = np.argwhere(self.aligned_arrays["so2-rf"].data > 0)
        _idx_temp = np.argwhere(self.aligned_arrays["so2-temperature"].data > 0)
        so2 = self.aligned_arrays["so2-rf"].data[_idx_rf].flatten()
        icefrac_v = self.aligned_arrays["icefrac"].data[_idx_rf].flatten()
        rf_v = self.aligned_arrays["rf"].data[_idx_rf].flatten()
        surfacetemp_v = self.aligned_arrays["surfacetemp"].data[_idx_rf].flatten()
        temp_v = self.aligned_arrays["temperature"].data[_idx_temp].flatten()
        _ids = so2.argsort()
        self._so2_peaks = so2[_ids]
        self._icefrac_peaks = icefrac_v[_ids]
        self._rf_peaks = rf_v[_ids]
        self._surfacetemp_peaks = surfacetemp_v[_ids]
        self._temperature_peaks = temp_v[_ids]
