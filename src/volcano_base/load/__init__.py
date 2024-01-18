"""Initialise the load module."""

from volcano_base.load.load_c2w_files import FindFiles
from volcano_base.load.load_historic_so2 import (
    get_so2_ob16_full_timeseries,
    get_so2_ob16_peak_timeseries,
)

__all__ = ["get_so2_ob16_full_timeseries", "get_so2_ob16_peak_timeseries", "FindFiles"]
