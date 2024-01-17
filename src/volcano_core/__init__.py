"""Initializes the package volcano-long-run."""

from importlib.metadata import version

from volcano_core import config, down, load, manipulate

__all__ = [
    "config",
    "down",
    "load",
    "manipulate",
]

__version__ = version(__package__)
