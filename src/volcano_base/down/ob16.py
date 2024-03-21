"""Download output data from Otto-Bliesner et al. 2016."""

import pathlib
from typing import Literal

import numpy as np
import xarray as xr
from returns.maybe import Maybe, Nothing, Some

import volcano_base

_MISSING_FILES = 0


def save_to_npz(just_looking: bool = True) -> None:
    """Save the OB16 data to .npz files."""
    # Combine and convert the datasets and save to compressed .npz files.
    path = volcano_base.config.DATA_PATH / "cesm-lme"
    if not path.exists():
        path.mkdir(parents=False)
    _save_output_files_to_npz(path, "h0", just_looking)
    _save_output_files_to_npz(path, "h1", just_looking)
    if just_looking and not globals()["_MISSING_FILES"]:
        print(
            "All files are present, and you are ready to convert them to .npz format!"
            " Run `save_to_npz` with `just_looking` set to False."
        )


def _look_for_files(file: pathlib.Path, just_looking: bool) -> Maybe[pathlib.Path]:
    if not file.exists():
        if globals()["_MISSING_FILES"] == 0:
            print(
                f"I went looking for files in {file.resolve().parent} but could not"
                " find any. Download manually from"
                " https://www.cesm.ucar.edu/community-projects/lme/data-sets"
                " (login needed)\nMissing files:"
            )
        print(f"\t{file.name}")
        globals()["_MISSING_FILES"] += 1
        return Nothing
    return Nothing if just_looking else Some(file)


def _save_output_files_to_npz(
    path: pathlib.Path, freq: Literal["h0", "h1"], just_looking: bool
) -> None:
    file0 = "b.e11.BLMTRC5CN.f19_g16.VOLC_GRA.00"
    ctrl_file0 = "b.e11.BLMTRC5CN.f19_g16.850forcing.003"
    match freq:
        case "h0":  # monthly
            file_tup = (
                path,
                file0,
                ".cam.h0.",
                ".085001-184912.nc",
                ".185001-200512.nc",
            )
            ctrl_file_tup = (
                path,
                ctrl_file0,
                ".cam.h0.",
                ".085001-184912.nc",
                ".185001-200512.nc",
            )
            save_modifier = "-monthly"
        case "h1":  # daily
            file_tup = (
                path,
                file0,
                ".cam.h1.",
                ".08500101-18491231.nc",
                ".18500101-20051231.nc",
            )
            ctrl_file_tup = (
                path,
                ctrl_file0,
                ".cam.h1.",
                ".08500101-18491231.nc",
                ".18500101-20051231.nc",
            )
            save_modifier = ""
        case _:
            volcano_base.never_called(freq)
    # Temperature.
    _download_ensemble("TREFHT", save_modifier, just_looking, file_tup)
    # RF forcing
    _download_ensemble("FSNTOA", save_modifier, just_looking, file_tup)
    # Control run for temperature.
    _download_ctrl_run("TREFHT", save_modifier, just_looking, ctrl_file_tup)
    # Control run for RF forcing.
    _download_ctrl_run("FSNTOA", save_modifier, just_looking, ctrl_file_tup)


def _download_ctrl_run(
    variable: Literal["FSNTOA", "TREFHT"],
    save_modifier,
    just_looking,
    file_tup,
) -> None:
    path, ctrl_file0, cam, range0, range1 = file_tup
    ctrl_filename_0 = f"{ctrl_file0}{cam}{variable}{range0}"
    ctrl_filename_1 = f"{ctrl_file0}{cam}{variable}{range1}"
    match (
        _look_for_files(path / ctrl_filename_0, just_looking),
        _look_for_files(path / ctrl_filename_1, just_looking),
    ):
        case (Some(file_0), Some(file_1)):
            if not (
                out_file := (
                    path / f"{variable}850forcing-control{save_modifier}-003.npz"
                )
            ).exists():
                print(f"Saving to {out_file}...")
                data = xr.open_mfdataset([file_0, file_1])
                array = volcano_base.manipulate.mean_flatten(
                    data[variable], dims=["lat", "lon"]
                )
                np.savez(
                    out_file,
                    data=array.data,
                    times=array.time.data,
                )
        case _:
            pass


def _download_ensemble(
    variable: Literal["FSNTOA", "TREFHT"],
    save_modifier,
    just_looking,
    file_tup,
) -> None:
    for i in range(5):
        match (
            _look_for_files(
                file_tup[0]
                / (file_tup[1] + str(i + 1) + file_tup[2] + variable + file_tup[3]),
                just_looking,
            ),
            _look_for_files(
                file_tup[0]
                / (file_tup[1] + str(i + 1) + file_tup[2] + variable + file_tup[4]),
                just_looking,
            ),
        ):
            case (Some(file_0), Some(file_1)):
                if (
                    out_file := (
                        file_tup[0] / f"{variable}{save_modifier}-00{i + 1}.npz"
                    )
                ).exists():
                    continue
                print(f"Saving to {out_file}...")
                data = xr.open_mfdataset([file_0, file_1])
                array = volcano_base.manipulate.mean_flatten(
                    data[variable], dims=["lat", "lon"]
                )
                np.savez(
                    out_file,
                    data=array.data,
                    times=array.time.data,
                )
            case _:
                pass


if __name__ == "__main__":
    save_to_npz(True)
