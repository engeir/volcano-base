"""Initialise download module."""

from volcano_base.down import cesm2
from volcano_base.down.historic_so2 import save_historical_so2

__all__ = ["save_historical_so2", "cesm2"]
