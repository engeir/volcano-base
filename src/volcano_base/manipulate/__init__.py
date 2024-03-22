"""Initialise the manipulate module."""

from volcano_base.manipulate.time_series import (
    approx_align,
    data_array_operation,
    dt2float,
    float2dt,
    get_median,
    keep_whole_years,
    mean_flatten,
    normalize_peaks,
    remove_seasonality,
    sampling_rate,
    shift_arrays,
    subtract_climatology,
    subtract_mean_of_tail,
    weighted_season_avg,
    weighted_year_avg,
)

__all__ = [
    "approx_align",
    "data_array_operation",
    "dt2float",
    "float2dt",
    "get_median",
    "keep_whole_years",
    "mean_flatten",
    "normalize_peaks",
    "remove_seasonality",
    "sampling_rate",
    "shift_arrays",
    "subtract_climatology",
    "subtract_mean_of_tail",
    "weighted_season_avg",
    "weighted_year_avg",
]
