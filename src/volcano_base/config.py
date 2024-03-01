"""Configuration file for `volcano-base`."""

import pathlib
from typing import Literal, Never, NoReturn

import tomllib
from returns.result import Failure, Result, Success


def never_called(value: Never) -> NoReturn:
    """Raise an error if a value is passed to a function that should never be called."""
    # The function is useful when running mypy. If, in a series of if/elif or
    # match/case, a variable is not fully handled, mypy will complain and say that the
    # variable is of the wrong type when this function is called in the final `else`
    # clause.
    raise AssertionError("Code is unreachable.")


def ask_then_create(file_path: pathlib.Path) -> None:
    """Ask before creating a directory."""
    if file_path.exists():
        return
    # Ask user if it is ok to create config file here.
    ans = input(f"Is it okay to create {file_path.resolve()}? [y/N] ").lower()
    if ans in ["y", "yes"]:
        file_path.mkdir(parents=True)
    else:
        print("Okay, I will not create anything.")


def create_config() -> Result[pathlib.Path, str]:
    """Create the file where the configuration will be saved."""
    here = pathlib.Path(".")
    ask_then_create(_data := here / "downloaded_files")
    ask_then_create(_save := here / "generated_files")
    _cfg = here / "volcano-base.toml"
    if not _cfg.exists():
        ans = input(f"Is it okay to create {_cfg.resolve()}? [y/N] ").lower()
        if ans not in ["y", "yes"]:
            return Failure("No config file exists.")
        with open(_cfg.resolve(), mode="w") as cfg:
            _config_content(cfg, here, _data, _save)
    return Success(_cfg)


def _config_content(cfg, here, _data, _save):
    cfg.write("[volcano-base]\n")
    cfg.write("# Location of the repository\n")
    cfg.write(f'project_root = "{here.resolve()}"\n')
    cfg.write("# Location of the data used in analysis scripts\n")
    cfg.write(f'data_path = "{_data.resolve()}"\n')
    cfg.write("# Location of the saved figures\n")
    cfg.write(f'save_path = "{_save.resolve()}"')


match create_config():
    case Success(_cfg):
        pass
    case Failure(msg):
        raise FileNotFoundError(msg)
# https://github.com/python/mypy/issues/16423
with _cfg.open(mode="rb") as cfg:
    out = tomllib.load(cfg)
    PROJECT_ROOT = pathlib.Path(out["volcano-base"]["project_root"])
    DATA_PATH = pathlib.Path(out["volcano-base"]["data_path"])
    SAVE_PATH = pathlib.Path(out["volcano-base"]["save_path"])
    # data_path = "/media/een023/LaCie/een023/cesm/model-runs"

MEANS: dict[Literal["TREFHT"], float] = {"TREFHT": 287.37903283}
DATA_ATTRS = {
    "AODVISstdn": ["Stratospheric aerosol optical depth 550 nm day night", "1"],
    "FSNTOA": ["Net solar flux at top of atmosphere", "W/m2"],
    "TREFHT": ["Reference height temperature", "K"],
    "so4_a1": ["so4_a1 concentration", "kg/kg"],
    "so4_a2": ["so4_a2 concentration", "kg/kg"],
    "so4_a3": ["so4_a3 concentration", "kg/kg"],
    "TROP_P": ["Tropopause Pressure", "Pa"],
    "TMSO2": ["SO2 burden", "Tg"],
    "FLUT": ["Upwelling longwave flux at top of model", "W/m2"],
    "FLNT": ["Net longwave flux at top of model", "W/m2"],
    "FSNT": ["Net solar flux at top of model", "W/m2"],
    "FLNS": ["Net longwave flux at surface", "W/m2"],
    "SO2": ["SO2 concentration", "mol/mol"],
    "SST": ["sea surface temperature", "K"],
    "T": ["Temperature", "K"],
    "U": ["Zonal wind", "m/s"],
}
