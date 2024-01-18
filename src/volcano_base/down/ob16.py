"""Download output data from Otto-Bliesner et al. 2016."""

import pathlib

import numpy as np
import xarray as xr
from returns.maybe import Maybe, Some

import volcano_base

_MISSING_FILES = 0


def save_to_npz() -> None:
    """Save the OB16 data to .npz files."""
    # Combine and convert the datasets and save to compressed .npz files.
    path = volcano_base.config.DATA_PATH / "cesm-lme"
    if not path.exists():
        path.mkdir(parents=False)
    _save_output_files_to_npz(path)


def _look_for_files(file: pathlib.Path) -> Maybe[pathlib.Path]:
    if not file.exists():
        if globals()["_MISSING_FILES"] == 0:
            print(
                f"I went looking for files in {file.resolve().parent} but could not"
                " find any. Download manually from"
                " https://www.earthsystemgrid.org/dataset/ucar.cgd.cesm2le.atm.proc.daily_ave.html"
                " (login needed)\nMissing files:"
            )
        print(f"\t{file.name}")
        globals()["_MISSING_FILES"] += 1
    return Maybe(file)


def _save_output_files_to_npz(path: pathlib.Path) -> None:
    file0 = "b.e11.BLMTRC5CN.f19_g16.VOLC_GRA.00"
    file1 = ".cam.h0."
    file2_0 = ".08500101-18491231.nc"
    file2_1 = ".18500101-20051231.nc"
    # Temperature.
    for i in range(5):
        match (
            _look_for_files(path / (file0 + str(i + 1) + file1 + "TREFHT" + file2_0)),
            _look_for_files(path / (file0 + str(i + 1) + file1 + "TREFHT" + file2_1)),
        ):
            case (Some(file_0), Some(file_1)):
                data = xr.open_mfdataset([file_0, file_1])
                array = volcano_base.manipulate.mean_flatten(
                    data["TREFHT"], dims=["lat", "lon"]
                )
                np.savez(
                    path / f"TREFHT-00{i+1}", data=array.data, times=array.time.data
                )
            case _:
                pass
    # RF forcing
    for i in range(5):
        match (
            _look_for_files(path / (file0 + str(i + 1) + file1 + "FSNTOA" + file2_0)),
            _look_for_files(path / (file0 + str(i + 1) + file1 + "FSNTOA" + file2_1)),
        ):
            case (Some(file_0), Some(file_1)):
                data = xr.open_mfdataset([file_0, file_1])
                array = volcano_base.manipulate.mean_flatten(
                    data["FSNTOA"], dims=["lat", "lon"]
                )
                np.savez(
                    path / f"FSNTOA-00{i+1}", data=array.data, times=array.time.data
                )
            case _:
                pass
    # Control run for temperature.
    filename_0 = (
        "b.e11.BLMTRC5CN.f19_g16.850forcing.003.cam.h0.TREFHT.08500101-18491231.nc"
    )
    filename_1 = (
        "b.e11.BLMTRC5CN.f19_g16.850forcing.003.cam.h0.TREFHT.18500101-20051231.nc"
    )
    match (_look_for_files(path / filename_0), _look_for_files(path / filename_1)):
        case (Some(file_0), Some(file_1)):
            data = xr.open_mfdataset([file_0, file_1])
            array = volcano_base.manipulate.mean_flatten(
                data["TREFHT"], dims=["lat", "lon"]
            )
            np.savez(
                path / "TREFHT850forcing-control-003.npz",
                data=array.data,
                times=array.time.data,
            )
        case _:
            pass


if __name__ == "__main__":
    # path = volcano_base.config.DATA_PATH / "cesm-lme"
    # if not path.exists():
    #     path.mkdir(parents=False)
    # _save_output_files_to_npz(path)
    save_to_npz()
