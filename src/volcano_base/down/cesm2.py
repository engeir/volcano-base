r"""Download files from the CESM2 model.

All files are available form the archive at
https://archive.sigma2.no/pages/public/datasetDetail.jsf?id=10.11582/2024.00034.

A one-liner to download all files from the archive in bash: (requires lynx, rg, sed,
xargs and wget)

    lynx -dump -listonly https://ns9999k.webs.sigma2.no/10.11582_2024.00034/single-volcano-ensembles/ | rg '.*(?:nc|md)$' | sed 's/.*\s//' | xargs wget {}
"""

import pathlib
import sys

import requests
import rich
import urllib3
from bs4 import BeautifulSoup

import volcano_base

# URL of the remote index.html file
_URL = "https://ns9999k.webs.sigma2.no/10.11582_2024.00034/single-volcano-ensembles/"


def _find_files() -> list[str]:
    # Fetch the HTML content of the remote file
    response = requests.get(_URL, verify=False)
    html_content = response.text
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    # Find all 'a' tags (anchor tags) with 'href' attribute
    href_tags = soup.find_all("a", href=True)
    # Extract the 'href' attribute and corresponding link for each tag
    files = []
    for tag in href_tags:
        link = tag.get("href")
        if link.endswith(".nc") or link.endswith(".md"):
            files.append(link)
            # print(_URL + link)
    return files


def save_cesm_files(path: pathlib.Path) -> None:
    """Save the CESM2 NIRD archive files to disk.

    This function is used by functions inside the `volcano_base.load` module, and should
    not be needed to be called by the user.

    Parameters
    ----------
    path : pathlib.Path
        Path to the file to download.
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if not path.exists():
        path.mkdir(parents=False)
    answer = input(
        f"Is it ok that I download all CESM2 NIRD archive files to {path.resolve()}? [y/N] "
    ).lower()
    if answer not in ["y", "yes"]:
        sys.exit(
            "Ok, I will not download anything. The files are needed to run the script,"
            f" and can be downloaded manually from {_URL}."
        )
    for file in _find_files():
        # Input file with injected SO2.
        _download_cesm_file(path, file)
    print("Done!")


def _download_cesm_file(path: pathlib.Path, file_name: str) -> None:
    file = path / file_name
    url = f"{_URL}{file_name}"
    if file.exists():
        print(
            f"{file} already exists, so I skip this. Delete it first if you are"
            " sure you want to download it again."
        )
        return
    progress = rich.progress.Progress(
        rich.progress.TextColumn("[progress.description]Downloading..."),
        rich.progress.SpinnerColumn(),
        rich.progress.BarColumn(),
        rich.progress.TaskProgressColumn(),
        rich.progress.MofNCompleteColumn(),
        rich.progress.TimeRemainingColumn(elapsed_when_finished=True),
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
    }
    with requests.get(url, stream=True, verify=False, headers=headers) as r:
        # Check if response is OK (status code 200)
        r.raise_for_status()
        total_length = r.headers.get("Content-Length")
        chunk_size = 8192
        total = int(total_length) // chunk_size if total_length is not None else 0
        with progress:
            progress.console.print(f"[progress.description]Downloading {file_name}")
            with open(file, "wb") as f:
                for chunk in progress.track(
                    r.iter_content(chunk_size=chunk_size),
                    # total=20851,
                    total=total,
                    description=f"[cyan]Downloading {file_name}",
                ):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)


def _main() -> None:
    path: pathlib.Path = volcano_base.config.DATA_PATH / "nird-archive"
    save_cesm_files(path)


if __name__ == "__main__":
    _main()
