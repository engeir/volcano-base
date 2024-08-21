"""Load data from McGraw et al. (2024)."""

import pathlib

import volcano_base


def mcg24_archive_regex() -> volcano_base.load.RegexLookup:
    """Return a regex object that looks for files using the NIRD archive directory hierarchy."""
    regex = r"""# Match everything up to 'mcg2024'
        .*mcg2024/fig3a_ModelE2.2_Toba_ensemble_Tsurf_maps/
        (.*)
        _
        (.*)
        _
        (.*)
        _
        (.*)
        _
        (.*)
        _
        (.*)
        """
    group_names = {
        "Attribute": "attr",
        "Effective radius": "reff",
        "Ensemble": "ensemble",
        "Eruption month": "eruption",
        "Time": "time_period",
        "Mapping": "map",
    }
    reverse_search = (
        pathlib.Path("mcg2024")
        / "fig3a_ModelE2.2_Toba_ensemble_Tsurf_maps"
        / "<attr>_<reff>_<ensemble>_<eruption>_<time_period>_<map><ft>"
    )
    return volcano_base.load.RegexLookup(".nc", group_names, reverse_search, regex)


def find_mcg24_files() -> volcano_base.load.FindFiles:
    """Return an object that lists and loads all data from McGraw et al. (2024)."""
    return volcano_base.load.FindFiles(mcg24_archive_regex())
