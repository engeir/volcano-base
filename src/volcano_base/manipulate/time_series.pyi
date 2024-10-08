import numpy as np
import xarray as xr
from collections.abc import Callable as Callable
from typing import Literal, overload

def data_array_operation(arrays: list[xr.DataArray], operation: Callable[[xr.DataArray], xr.DataArray]) -> list: ...
def approx_align(*a: xr.DataArray) -> tuple[xr.DataArray, ...]: ...
def shift_arrays(arrays: list[xr.DataArray], ens: str | None = None, daily: bool = True, custom: list | int | None = None) -> list[xr.DataArray]: ...
@overload
def mean_flatten(arrays: list[xr.DataArray], dims: list[str] | None = None) -> list[xr.DataArray]: ...
@overload
def mean_flatten(arrays: xr.DataArray, dims: list[str] | None = None) -> xr.DataArray: ...
@overload
def remove_seasonality(arrays: list[xr.DataArray], freq: float = 1.0, radius: float = 0.01, plot: bool = False) -> list[xr.DataArray]: ...
@overload
def remove_seasonality(arrays: xr.DataArray, freq: float = 1.0, radius: float = 0.01, plot: bool = False) -> xr.DataArray: ...
def subtract_climatology(arr: xr.DataArray, clim_arr: xr.DataArray, groupby: Literal['time.dayofyear', 'time.month']) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray]: ...
def dt2float(arr: np.ndarray | xr.CFTimeIndex, days_in_year: int = 365) -> xr.CFTimeIndex: ...
def float2dt(arr: xr.CFTimeIndex | np.ndarray, freq: str = 'D') -> xr.CFTimeIndex: ...
def pressureheight2metricheight(pressure_coords: xr.DataArray | np.ndarray) -> xr.DataArray | np.ndarray: ...
def metricheight2pressureheight(metric_coords: xr.DataArray | np.ndarray) -> xr.DataArray | np.ndarray: ...
@overload
def get_median(arrays: list[xr.DataArray], xarray: Literal[True]) -> xr.DataArray: ...
@overload
def get_median(arrays: list[xr.DataArray], xarray: Literal[False]) -> tuple[np.ndarray, np.ndarray]: ...
@overload
def get_mean(arrays: list[xr.DataArray], xarray: Literal[True]) -> xr.DataArray: ...
@overload
def get_mean(arrays: list[xr.DataArray], xarray: Literal[False]) -> tuple[np.ndarray, np.ndarray]: ...
@overload
def keep_whole_years(arrays: list[xr.DataArray], freq: str = 'D') -> list[xr.DataArray]: ...
@overload
def keep_whole_years(arrays: xr.DataArray, freq: str = 'D') -> xr.DataArray: ...
def subtract_mean_of_tail(arrs: list, n_elements: int = 120) -> list: ...
def weighted_year_avg(da: xr.DataArray) -> xr.DataArray: ...
def weighted_season_avg(da: xr.DataArray) -> xr.DataArray: ...
def weighted_monthly_avg(da: xr.DataArray) -> xr.DataArray: ...
def normalize_peaks(*args: tuple[list | np.ndarray, str]) -> tuple[list, ...]: ...
def sampling_rate(dates: np.ndarray) -> float: ...
