"""Initialise the manipulate module."""

from volcano_base.manipulate.time_series import (
    dt2float,
    float2dt,
    get_median,
    keep_whole_years,
    mean_flatten,
    normalize_peaks,
    remove_seasonality,
    shift_arrays,
    weighted_season_avg,
    weighted_year_avg,
)

__all__ = [
    "shift_arrays",
    "mean_flatten",
    "remove_seasonality",
    "dt2float",
    "float2dt",
    "get_median",
    "keep_whole_years",
    "weighted_year_avg",
    "weighted_season_avg",
    "normalize_peaks",
]
