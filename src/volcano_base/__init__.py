"""Initializes the package volcano-long-run."""

try:
    from importlib.metadata import version
except Exception:
    from importlib_metadata import version  # type: ignore[no-redef]

from volcano_base import config, down, load, manipulate
from volcano_base.config import never_called

__all__ = ["config", "down", "load", "manipulate", "never_called"]

__version__ = version(__package__)
