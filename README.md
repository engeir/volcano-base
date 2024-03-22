# Core module for volcanic eruption simulation projects

<sup>Latest version: v1.8.0</sup> <!-- x-release-please-version -->

> [!WARNING]
>
> This README reflects the changes made to the main branch. For the most up to date
> documentation about the version you are using, see the README at the relevant tag.

This repository contains the core elements used across several independent volcanic
eruption studies. This include strategies for downloading necessary data, loading data
from files and doing simple general manipulations to the time series.

## Install

This project is published to [pypi](https://pypi.org). Install with you preferred
package manager, for example using `pip`:

```bash
pip install volcano-base
```

## Usage

The available modules are:

- `down` (download datasets)
- `load` (find and load local files)
- `manipulate` (make changes to time series)
