r"""Download data presented in McGraw et al. (2024).

All files are available form the archive at
https://doi.org/10.5281/zenodo.7083247.
"""

import pathlib
import tarfile
import zipfile

import requests

import volcano_base

_URL = "https://zenodo.org/api/records/7083247/files-archive"
save_path = volcano_base.config.DATA_PATH


def _find_files() -> None:
    try:
        response = requests.get(_URL)
    except OSError:
        print("No connection to the server!")
        return None
    ok_response = 200
    if response.status_code == ok_response:
        # Save dataset to file
        open(save_path / "mcg2024.zip", "wb").write(response.content)
    else:
        print("ZIP file request not successful!.")
        return None


def save_mcg24_files() -> None:
    """Save the CESM2 NIRD archive files to disk."""
    # Get the ZIP file
    if not pathlib.Path(save_path / "mcg2024.zip").exists():
        _find_files()

    # Unzip
    if not (mcg2024 := pathlib.Path(save_path / "mcg2024")).is_dir():
        mcg2024.mkdir()
        with zipfile.ZipFile(save_path / "mcg2024.zip", "r") as zip_ref:
            zip_ref.extractall(save_path / "mcg2024")
    (pathlib.Path(save_path) / "mcg2024.zip").unlink()

    if (
        fname := pathlib.Path(
            mcg2024 / "fig3a_ModelE2.2_Toba_ensemble_Tsurf_maps.tar.gz"
        )
    ).exists():
        tar = tarfile.open(fname, "r:gz")
        tar.extractall(path=mcg2024, filter="fully_trusted")
        tar.close()


if __name__ == "__main__":
    save_mcg24_files()
