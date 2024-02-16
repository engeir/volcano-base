"""Initialise the manipulate module."""

from volcano_base.manipulate.time_series import (
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
    subtract_mean_of_tail,
    weighted_season_avg,
    weighted_year_avg,
)

__all__ = [
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
    "subtract_mean_of_tail",
    "weighted_season_avg",
    "weighted_year_avg",
]
