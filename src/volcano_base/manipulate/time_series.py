"""Functions that modify (lists of) xarray DataArrays."""

import datetime
import os
import warnings
from collections import Counter
from collections.abc import Callable
from typing import Literal, overload

import cftime
import matplotlib.pyplot as plt
import numpy as np
import scipy
import xarray as xr


def data_array_operation(
    arrays: list[xr.DataArray], operation: Callable[[xr.DataArray], xr.DataArray]
) -> list:
    """Perform an operation on a list of xarray DataArrays.

    Wrap what you want to do with a single array in a function.

    Parameters
    ----------
    arrays : list[xr.DataArray]
        A list of xarray DataArrays to perform the operation on.
    operation : Callable[[xr.DataArray], xr.DataArray]
        A function that should be performed on the arrays.

    Returns
    -------
    list
        A list of modified xarray DataArrays.

    Examples
    --------
    Implement the subtract_mean_of_tail function, first for a single array, then pass it
    to data_array_operation.

    >>> def single_array_sub_tail(arr: xr.DataArray) -> xr.DataArray:
    ...     arr_ = arr[-120:]
    ...     arr.data = arr.data - arr_.mean().data
    ...     return arr
    >>> data_array_operation([xr.DataArray([1, 2, 3]), xr.DataArray([4, 5, 6])], single_array_sub_tail)
    """
    for i, arr in enumerate(arrays):
        arrays[i] = operation(arr)
    return arrays


def approx_align(*a: xr.DataArray) -> tuple[xr.DataArray, ...]:
    """Align the DataArrays by interpolating them to the same time axis.

    This is useful when you know that the time axes are similar, but not exactly the
    same values. For example monthly data, but where they differ by a few days.

    Parameters
    ----------
    *a : xr.DataArray
        Any number of xarray DataArrays to align.

    Returns
    -------
    tuple[xr.DataArray, ...]
        The same number of xarray DataArrays, but aligned to the same time axis.
    """
    return tuple(value.interp_like(a[0]) for value in a)


def shift_arrays(
    arrays: list[xr.DataArray],
    ens: str | None = None,
    daily: bool = True,
    custom: list | int | None = None,
) -> list[xr.DataArray]:
    """Shift arrays to make the eruption occur on Feb. 15, 1850.

    Parameters
    ----------
    arrays : list[xr.DataArray]
        A list of xarray DataArrays to shift.
    ens : str | None
        Choose to shift any list of arrays according to the given ens value. Possible
        values are 'ens1', 'ens2', 'ens3', 'ens4' and 'ens5'.
    daily : bool
        If the data has monthly resolution instead of daily, set this to False
    custom : list | int | None
        Choose a custom shift in days that will be applied to all arrays in the list. A
        positive number of 365 will for example shift all dates one year back: 1851 ->
        1850. If a list is given, it must have the same length as the input list of
        arrays. Default is None.

    Returns
    -------
    list[xr.DataArray]
        A list of shifted xarray Data Arrays.

    Raises
    ------
    ValueError
        If the weighting on the first and fifth elements is not between 0 and 1.
    """
    array = arrays[:]
    match custom:
        case None:
            pass
        case int():
            custom_ = [custom] * len(array)
        case list():
            if len(custom) != len(array):
                raise ValueError(
                    "The custom shift list must have the same length as the input"
                    " list of arrays."
                )
            custom_ = custom
    for i, arr in enumerate(array):
        case_0 = arr.attrs["ensemble"] if ens is None else ens
        match case_0:
            case "ens1":
                shift = 0
            case "ens2":
                # From Feb 15 to May 15
                shift = 89 if daily else 3
            case "ens3":
                # From Fev 15 to Aug 15
                shift = 181 if daily else 6
            case "ens4":
                # From Feb 15 to Nov 15
                shift = 273 if daily else 9
            case "ens5":
                # From Feb 15 to Feb 15
                shift = 365 if daily else 12
            case _:
                if custom is None:
                    _warn_skips = (os.path.dirname(__file__),)
                    warnings.warn(  # noqa: B028
                        "I don't know how to shift this array. Using 0 as default. Note"
                        " that you may set a custom shift with the `custom` keyword.",
                        skip_file_prefixes=_warn_skips,
                    )
                shift = 0
        shift = shift if custom is None else custom_[i]
        if isinstance(arr.time.data[0], float):
            array[i] = arr.shift(time=-shift).dropna("time")
        else:
            array[i] = arr.shift(time=-shift)
    return list(xr.align(*array))


def _latitude_mean(arr: xr.DataArray, lat: str) -> xr.DataArray:
    """Average over latitude with appropriate weighting."""
    lats = getattr(arr, lat)
    weights = np.cos(np.deg2rad(lats))
    weights.name = "weights"
    return arr.weighted(weights).mean(lat)


@overload
def mean_flatten(
    arrays: list[xr.DataArray], dims: list[str] | None = None
) -> list[xr.DataArray]: ...


@overload
def mean_flatten(
    arrays: xr.DataArray, dims: list[str] | None = None
) -> xr.DataArray: ...


def mean_flatten(
    arrays: list[xr.DataArray] | xr.DataArray,
    dims: list[str] | None = None,
    lat: str = "lat",
) -> list[xr.DataArray] | xr.DataArray:
    """Average over all longitudes/zonal dimension.

    Parameters
    ----------
    arrays : list[xr.DataArray] | xr.DataArray
        A list of xarray DataArrays to average over.
    dims : list[str] | None
        A list of strings with the dimensions that should be averaged out. Default is
        ["lon", "time"].
    lat : str
        The name that should be used for the latitude dimension. Default is 'lat'.

    Returns
    -------
    list[xr.DataArray] | xr.DataArray
        A list of averaged xarray Data Arrays.
    """
    if dims is None:
        dims = ["lon", "time"]
    try:
        # If latitude is included, it has to be treated with care to make up for
        # changes in grid cells.
        dims.remove(lat)
    except ValueError:
        include_lat = False
    else:
        include_lat = True
    if isinstance(arrays, xr.DataArray):
        if include_lat:
            tmp = _latitude_mean(arrays, lat)
            arrays = tmp.assign_attrs(arrays.attrs)
            tmp.close()
        arrays = arrays.mean(dim=dims)
        arrays = arrays.assign_attrs(arrays.attrs)
        return arrays
    array = arrays[:]
    for i, arr in enumerate(array):
        if include_lat:
            tmp = _latitude_mean(arr, lat)
            arr_ = tmp.assign_attrs(arr.attrs)
            tmp.close()
        else:
            arr_ = arr
        array[i] = arr_.mean(dim=dims)
        array[i] = array[i].assign_attrs(arr_.attrs)
        arr.close()
        arr_.close()
    return array


@overload
def remove_seasonality(
    arrays: list[xr.DataArray],
    freq: float = 1.0,
    radius: float = 0.01,
    plot: bool = False,
) -> list[xr.DataArray]: ...


@overload
def remove_seasonality(
    arrays: xr.DataArray,
    freq: float = 1.0,
    radius: float = 0.01,
    plot: bool = False,
) -> xr.DataArray: ...


def remove_seasonality(
    arrays: list[xr.DataArray] | xr.DataArray,
    freq: float = 1.0,
    radius: float = 0.01,
    plot: bool = False,
) -> list[xr.DataArray] | xr.DataArray:
    """Remove seasonality from array.

    Parameters
    ----------
    arrays : list[xr.DataArray] | xr.DataArray
        An array or a list of arrays to remove seasonality from
    freq : float
        Gives the frequency that should be removed when using the Fourier method
    radius : float
        Gives the frequency range that should be removed when using the Fourier method
    plot : bool
        Will plot what is removed in the Fourier domain

    Returns
    -------
    list[xr.DataArray] | xr.DataArray
        An object of the same arrays as the input, but modified
    """
    if isinstance(arrays, xr.DataArray):
        return _remove_seasonality_fourier(arrays.copy(), freq, radius, plot)
    array = arrays[:]
    for i, arr in enumerate(array):
        # Need to re-assign `arr`, otherwise it will be re-used
        array[i] = _remove_seasonality_fourier(arr, freq, radius, plot)
    return array[:]


def _remove_seasonality_fourier(
    arr: xr.DataArray, freq: float, radius: float, plot: bool
) -> xr.DataArray:
    """Remove seasonality via Fourier transform.

    Parameters
    ----------
    arr : xr.DataArray
        An xarray DataArray.
    freq : float
        Give a custom frequency that should be removed. Default is 1.
    radius : float
        Give a custom radius that should be removed. Default is 0.01.
    plot : bool
        Will plot what is removed in the Fourier domain

    Returns
    -------
    xr.DataArray
        An xarray DataArray.

    Raises
    ------
    TypeError
        If the time axis type is not recognised and we cannot translate to frequency.
    """
    if isinstance(arr.time.data[0], float):
        sample_spacing = arr.time.data[1] - arr.time.data[0]
    elif isinstance(arr.time.data, xr.CFTimeIndex | np.ndarray) and isinstance(
        arr.time.data[0], cftime.datetime
    ):
        sec_in_year = 3600 * 24 * 365
        sample_spacing = (
            arr.time.data[11] - arr.time.data[10]
        ).total_seconds() / sec_in_year
    else:
        raise TypeError(
            f"I cannot handle time arrays where {type(arr.time.data) = } and"
            f" {type(arr.time.data[0]) = }. The array must be a numpy.ndarray or"
            " xr.CFTimeIndex, and the elements must be floats or cftime.datetime."
        )
    n = len(arr.time.data)
    yf = scipy.fft.rfft(arr.data)
    xf = scipy.fft.rfftfreq(n, sample_spacing)
    idx = np.argwhere((xf > freq - radius) & (xf < freq + radius))
    yf_clean = yf.copy()
    if any(idx):
        linear_fill = np.linspace(
            yf_clean[idx[0] - 1], yf_clean[idx[-1] + 1], len(yf_clean[idx])
        )
        yf_clean[idx] = linear_fill
    else:
        print(
            "Warning: No frequencies were removed! The radius is probably too small,"
            " try with a larger one."
        )
        print(
            "HINT: You can also view the before/after of this function by pasing in"
            " the `plot=True` keyword argument."
        )
    new_f_clean = scipy.fft.irfft(yf_clean)
    if plot:
        plt.figure()
        plt.semilogy(xf, np.abs(yf))
        plt.semilogy(xf, np.abs(yf_clean))
        plt.xlim([-1, 10])
        plt.show()
    arr.data[: len(new_f_clean)] = new_f_clean

    return arr[:]


def subtract_climatology(
    arr: xr.DataArray,
    clim_arr: xr.DataArray,
    groupby: Literal["time.dayofyear", "time.month"],
) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray]:
    """Subtract the climatological mean.

    Parameters
    ----------
    arr : xr.DataArray
        The data array to subtract the climatology from.
    clim_arr : xr.DataArray
        The climatology data array to take the climatology from.
    groupby : Literal["time.dayofyear", "time.month"]
        The groupby string to use when grouping the data. At the moment, only daily and
        monthly resolved data is supported.

    Returns
    -------
    xr.DataArray
        The corrected data array with the climatology subtracted.
    xr.DataArray
        The raw data array with the climatology subtracted.
    xr.DataArray
        The climatology data array, aligned with the two other arrays.

    Examples
    --------
    Let us say you have many arrays that you want to subtract the climatology from. You
    may then want to combine this function with `data_array_operation`. However,
    `data_array_operation` expects a function that takes a single array as input and
    returns the same array with the operation performed. We therefore need to wrap the
    `subtract_climatology` function in a function.

    >>> t = xr.cftime_range(
    ...     start="1850-01-01",
    ...     periods=100,
    ...     calendar="noleap",
    ...     freq="MS",
    ... )
    >>> clim_arr = xr.DataArray(np.arange(100), dims=["time"], coords={"time": t})
    >>> def single_array_sub_clim(arr: xr.DataArray) -> xr.DataArray:
    ...     return subtract_climatology(arr, clim_arr, "time.month")[0]
    >>> data_array_operation([clim_arr, clim_arr], single_array_sub_clim)
    """
    clim_arr, arr = xr.align(clim_arr, arr)
    climatology_ = clim_arr.groupby(groupby)
    climatology = (
        climatology_.mean("time") if "month" in groupby else climatology_.mean()
    )
    return (
        arr.groupby(groupby) - climatology,
        clim_arr.groupby(groupby) - climatology,
        clim_arr,
    )


def dt2float(
    arr: np.ndarray | xr.CFTimeIndex, days_in_year: int = 365
) -> xr.CFTimeIndex:
    """Set new time coordinates to floats from an array of datetime objects.

    Parameters
    ----------
    arr : np.ndarray | xr.CFTimeIndex
        Array that should be re-set
    days_in_year : int
        Number of days in the year used by the xr.CFTimeIndex object

    Returns
    -------
    xr.CFTimeIndex
        Input array with re-set time coordinates as cftime_range
    """
    if not isinstance(arr, xr.CFTimeIndex):
        arr = xr.CFTimeIndex(arr)
    x_out: xr.CFTimeIndex = arr.map(lambda x: x.toordinal() / days_in_year)
    return x_out


def float2dt(arr: xr.CFTimeIndex | np.ndarray, freq: str = "D") -> xr.CFTimeIndex:
    """Set new time coordinates with daily frequency from array of floats.

    The function assumes that the original time coordinates is a simple floating point
    number array, with one event per day in a 'noleap' calendar, starting on January 1.

    Parameters
    ----------
    arr : xr.CFTimeIndex | np.ndarray
        Array that should be re-set
    freq : str
        The frequency of the datetime array. 'D' gives daily and 'MS' gives monthly,
        beginning of the month. See
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
        for a full list of allowed frequencies.

    Returns
    -------
    xr.CFTimeIndex
        Input array with re-set time coordinates as cftime_range
    """
    init = int(arr[0])
    init_str = "0" * (4 - len(str(init))) + str(init)
    return xr.cftime_range(
        start=init_str, periods=len(arr), calendar="noleap", freq=freq
    )


@overload
def get_median(arrays: list[xr.DataArray], xarray: Literal[True]) -> xr.DataArray: ...


@overload
def get_median(
    arrays: list[xr.DataArray], xarray: Literal[False]
) -> tuple[np.ndarray, np.ndarray]: ...


def get_median(
    arrays: list[xr.DataArray], xarray: bool = False
) -> tuple[np.ndarray, np.ndarray] | xr.DataArray:
    """Get the median across all arrays in `arrays`.

    Parameters
    ----------
    arrays : list[xr.DataArray]
        A list of xarray DataArrays to shift.
    xarray : bool
        Return the array as a data array, using the meta data of the first element of
        ``arrays``.

    Returns
    -------
    tuple[np.ndarray, np.ndarray] | xr.DataArray
        First and second axis with the median of the arrays.

    Notes
    -----
    The arrays are assumed to be correctly aligned, consider running `shift_arrays` on
    them before obtaining the median from this function.
    """
    array = arrays[:]
    x_ax = array[0].time
    y_ax = np.zeros((len(array), len(array[0].data)))
    for i, arr in enumerate(array):
        y_ax[i, :] = arr[:].data
    if xarray:
        out = array[0].copy()
        out.data = np.median(y_ax, axis=0)
        out = out.assign_coords(time=x_ax)
        out = out.assign_attrs(array[0].attrs)
        return out
    return x_ax, np.median(y_ax, axis=0)


@overload
def keep_whole_years(
    arrays: list[xr.DataArray], freq: str = "D"
) -> list[xr.DataArray]: ...


@overload
def keep_whole_years(arrays: xr.DataArray, freq: str = "D") -> xr.DataArray: ...


def keep_whole_years(
    arrays: list[xr.DataArray] | xr.DataArray,
    freq: str = "D",
) -> list[xr.DataArray] | xr.DataArray:
    """Keep only whole years.

    Useful as a pre-processing step before the ``weighted_year_avg`` function.

    Parameters
    ----------
    arrays : list[xr.DataArray] | xr.DataArray
        Array or a list of arrays to shorten.
    freq : str
        The frequency of the time coordinate

    Returns
    -------
    list[xr.DataArray] | xr.DataArray
        Same type as the input and shorten to only include full years.

    Notes
    -----
    Warning: This function uses the middle year as a reference of the "correct" number
    of events in a given year. This means that if the time series include years of
    irregular lengths, for example with leap years, this function will not work.
    """
    if isinstance(arrays, xr.DataArray):
        return _keep_whole_years(arrays, freq=freq)
    arr = arrays[:]
    for i, v in enumerate(arr):
        arr[i] = _keep_whole_years(v, freq=freq)
    return arr[:]


def _keep_whole_years(arr: xr.DataArray, freq: str = "D") -> xr.DataArray:
    try:
        _ = arr.time.dt.year
    except Exception:
        arr = arr.assign_coords(time=float2dt(arr.time, freq=freq))
    counts = Counter(list(arr.time.dt.year.data))
    # We here assume that the middle is not the edge (i.e., we should have an array
    # spanning more than three years), and that the middle year has the correct amount
    # of elements for any given year. This also means that calendars with leap days will
    # note work.
    norm_amount = list(counts.values())[len(list(counts)) // 2]
    valid_years = [i for i, v in counts.items() if v == norm_amount]
    arr = arr.sel(time=arr.time.dt.year.isin(valid_years))
    return arr


def subtract_mean_of_tail(arrs: list, n_elements: int = 120) -> list:
    """Subtract the mean of the tail of the arrays.

    Parameters
    ----------
    arrs : list
        List of arrays to subtract the mean from.
    n_elements : int
        Number of elements to subtract the mean from. Default is 120, one decade of
        monthly data.

    Returns
    -------
    list
        List of arrays with the mean subtracted.
    """
    # Subtract the mean of the last decade
    for i, arr in enumerate(arrs):
        arr_ = arr[-n_elements:]
        arr.data = arr.data - arr_.mean().data
        arrs[i] = arr
    return arrs


def weighted_year_avg(da: xr.DataArray) -> xr.DataArray:
    """Calculate a temporal mean, weighted by days in each month.

    Parameters
    ----------
    da : xr.DataArray
        Input data structure to do temporal average on

    Returns
    -------
    xr.DataArray
        The new data structure with time averaged data

    Notes
    -----
    From
    https://ncar.github.io/esds/posts/2021/yearly-averages-xarray/#wrap-it-up-into-a-function
    """
    # Determine the month length
    month_length = da.time.dt.days_in_month
    # Calculate the weights
    wgts = month_length.groupby("time.year") / month_length.groupby("time.year").sum()
    # Make sure the weights in each year add up to 1
    np.testing.assert_allclose(wgts.groupby("time.year").sum(xr.ALL_DIMS), 1.0)
    # Setup our masking for nan values
    cond = da.isnull()
    ones = xr.where(cond, 0.0, 1.0)
    # Calculate the numerator
    obs_sum = (da * wgts).resample(time="YS").sum(dim="time")
    # Calculate the denominator
    ones_out = (ones * wgts).resample(time="YS").sum(dim="time")
    # Return the weighted average
    return obs_sum / ones_out


def weighted_season_avg(da: xr.DataArray) -> xr.DataArray:
    """Calculate a temporal mean, weighted by days in each month.

    Parameters
    ----------
    da : xr.DataArray
        Input data structure to do temporal average on

    Returns
    -------
    xr.DataArray
        The new data structure with time averaged data

    Notes
    -----
    From
    https://ncar.github.io/esds/posts/2021/yearly-averages-xarray/#wrap-it-up-into-a-function
    """
    # Determine the month length
    month_length = da.time.dt.days_in_month
    # Calculate the weights
    wgts = (
        month_length.groupby("time.season") / month_length.groupby("time.season").sum()
    )
    # Make sure the weights in each year add up to 1
    np.testing.assert_allclose(wgts.groupby("time.season").sum(xr.ALL_DIMS), np.ones(4))
    # Setup our masking for nan values
    cond = da.isnull()
    ones = xr.where(cond, 0.0, 1.0)
    # Calculate the numerator
    obs_sum = (da * wgts).resample(time="QS").sum(dim="time")
    # Calculate the denominator
    ones_out = (ones * wgts).resample(time="QS").sum(dim="time")
    # Return the weighted average
    return obs_sum / ones_out


def weighted_monthly_avg(da: xr.DataArray) -> xr.DataArray:
    """Calculate a temporal mean, weighted by days in each month.

    Parameters
    ----------
    da : xr.DataArray
        Input data structure to do temporal average on

    Returns
    -------
    xr.DataArray
        The new data structure with time averaged data

    Notes
    -----
    From
    https://ncar.github.io/esds/posts/2021/yearly-averages-xarray/#wrap-it-up-into-a-function
    """
    # Determine the month length
    month_length = da.time.dt.days_in_month
    # Calculate the weights
    wgts = month_length.groupby("time.month") / month_length.groupby("time.month").sum()
    # Make sure the weights in each year add up to 1
    np.testing.assert_allclose(wgts.groupby("time.month").sum(xr.ALL_DIMS), np.ones(12))
    # Setup our masking for nan values
    cond = da.isnull()
    ones = xr.where(cond, 0.0, 1.0)
    # Calculate the numerator
    obs_sum = (da * wgts).resample(time="MS").sum(dim="time")
    # Calculate the denominator
    ones_out = (ones * wgts).resample(time="MS").sum(dim="time")
    # Return the weighted average
    return obs_sum / ones_out


def normalize_peaks(*args: tuple[list | np.ndarray, str]) -> tuple[list, ...]:
    """Normalize the input arrays.

    The string (see description of `args` in the parameters section) only negates the
    arrays. Completely pointless actually, since this should rather be done after the
    fact, but also why not.

    Parameters
    ----------
    *args : tuple[list | np.ndarray, str]
        Each tuple sent to `args` contains an array and a string describing if the array
        is an AOD or RF array. But really the only difference is that is the string is
        `aod` we multiply by `1`, and if the string is `rf` we multiply by -1.

    Returns
    -------
    tuple[list, ...]
        However many tuples with arrays are sent in, as many lists are returned
    """
    out: list[list] = []
    win_length = 12
    for tup in args:
        arrs = []
        for i in range(len(tup[0])):
            array = scipy.signal.savgol_filter(tup[0][i].data, win_length, 3)
            if tup[1] == "aod":
                scaled_array = tup[0][i] / array.max()
            elif tup[1] == "rf":
                scaled_array = -tup[0][i] / array.min()
            arrs.append(scaled_array)
        out.append(arrs)
    return tuple(out)


def sampling_rate(dates: np.ndarray) -> float:
    """Find the sampling rate.

    Parameters
    ----------
    dates : np.ndarray
        An array of dates. The dates can be in the following formats:
        - float
        - datetime.datetime
        - cftime._cftime.DatetimeNoLeap

    Returns
    -------
    float
        The sampling rate.

    Raises
    ------
    TypeError
        If the input date format is unknown.
    """
    match dates[0]:
        case float():
            return np.mean(np.diff(dates))
        case datetime.datetime():
            return np.mean(
                np.diff(
                    [
                        eval(datetime.datetime.strftime(i, "%Y+%-m/12+%-d/365"))
                        for i in dates
                    ]
                )
            )
        case cftime._cftime.DatetimeNoLeap():
            cftime2float_ = dt2float(dates)
            return np.mean(np.diff(cftime2float_))
        case _:
            raise TypeError(
                f"The input date format is unknown, found {type(dates[0]) = }"
            )
