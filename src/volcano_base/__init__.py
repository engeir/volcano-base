"""Initializes the package volcano-long-run."""

from importlib.metadata import version

from volcano_base import config, down, load, manipulate
from volcano_base.config import never_called

__all__ = ["config", "down", "load", "manipulate", "never_called"]

__version__ = version(__package__)
