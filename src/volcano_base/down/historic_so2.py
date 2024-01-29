"""Download historic SO2 file."""

import pathlib
import sys

import requests
import rich.progress

import volcano_base


def save_historical_so2(file: pathlib.Path) -> None:
    """Save the historic SO2 injections data to .npz files.

    This function is used by functions inside the `volcano_base.load` module, and should
    not be needed to be called by the user.

    Parameters
    ----------
    file : pathlib.Path
        Path to the file to download.

    Notes
    -----
    Used by Otto-Bliesner et al. (2016).
    """
    # Combine and convert the datasets and save to compressed .npz files.
    # path = vlr.config.DATA_PATH
    path = file.parent
    if not path.exists():
        path.mkdir(parents=False)
    # Input file with injected SO2.
    _download_so2_file(file)
    print(
        f"You might want to clean up the .nc files in {volcano_base.config.PROJECT_ROOT}."
    )


def _download_so2_file(file: pathlib.Path) -> None:
    if file.exists():
        print(
            f"{file} already exists, so I skip this. Delete it first if you are"
            " sure you want to download it again."
        )
        return
    url = f"https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/volc/{file.name}"
    answer = input(
        f"Is it ok that I download {file.name} to {file.parent}? [y/N] "
    ).lower()
    if answer not in ["y", "yes"]:
        sys.exit(
            "Ok, I will not download anything. The file is needed to run the script,"
            f" and can be downloaded manually from {url}."
        )
    progress = rich.progress.Progress(
        rich.progress.TextColumn("[progress.description]{task.description}"),
        rich.progress.SpinnerColumn(),
        rich.progress.BarColumn(),
        rich.progress.TaskProgressColumn(),
        rich.progress.MofNCompleteColumn(),
        rich.progress.TimeRemainingColumn(elapsed_when_finished=True),
    )
    with requests.get(url, stream=True, verify=False) as r:
        r.raise_for_status()
        with open(file, "wb") as f:
            with progress:
                for chunk in progress.track(
                    r.iter_content(chunk_size=8192),
                    total=20851,
                    description="[cyan]Downloading file...",
                ):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)
