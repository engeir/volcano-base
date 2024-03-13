"""Load all data files automatically."""

import pathlib
import re
from collections.abc import Iterable
from itertools import product
from typing import Self, overload

import numpy as np
import xarray as xr
from returns.result import Failure, Result, Success
from xarray.core.types import T_Xarray

import volcano_base


class FindFiles:
    """Find files that match a pre-defined regular expression.

    Parameters
    ----------
    ft : str
        file type to look for

    Attributes
    ----------
    _compset : set containing all component setups
    _sim : set containing all simulations
    _ens : set containing all ensembles
    _attr : set containing all attributes
    _freq : set containing all frequencies
    _date : set containing all dates
    _combined : set containing all combinations of the above sets that were found
    _bad_files : files that were candidates but that did not match the regex
    _matched_files : files that have been looked up among the files found with the regex
    _sort_order : tuple with the sorting that is applied to the files
    _sort_reverse : bool stating if the sorting of the files should be reversed

    Raises
    ------
    ConnectionError
        If the files cannot be found the hard disk might not be mounted

    Examples
    --------
    >>> ff = FindFiles()

    You find nothing since the date is wrong.

    >>> files = ff.find(
    ...     "h0", "e_BWma1850", "strong", "U", "ens1", "2x230828"
    ... )
    Traceback (most recent call last):
    ...
    AttributeError: ...
    >>> # [print(m) for m in files.get_files()]

    You still find nothing since there are two specifications of ensembles.

    >>> files = ff.find(
    ...     "h0", "e_BWma1850", "strong", "U", "ens1", "ens2"
    ... )
    Traceback (most recent call last):
    ...
    AttributeError: ...
    >>> # [print(m) for m in files]

    Now, you find all files with simulation type "strong" and ensemble type "ens2" and
    "ens4"

    >>> matches = ff.find("strong", ("ens2", "ens4"))
    >>> # [print(m) for m in matches.get_files().unwrap()]
    >>> # matches.print_files()
    >>> # print(len(matches))

    Remove ens1 and ens5 (none of them are present, but that's fine)

    >>> matches = matches.remove("ens1", "ens5")
    >>> # matches.print_files()
    >>> # print(len(matches))

    Keep h0, e_BWma1850 or e_fSST1850, FLNT or TREFHT or AODVISstdn and ens1 or ens2.

    >>> matches = matches.keep(
    ...    "h0",
    ...    ("e_BWma1850", "e_fSST1850"),
    ...    ["FLNT", "TREFHT", "AODVISstdn"],
    ...    {"ens1", "ens2"},
    ... )
    >>> # matches.print_files()
    >>> # print(len(matches))

    Load the files into xarray objects

    >>> xarrs = matches.load()
    >>> # [print(m) for m in xarrs]

    Or print the true file paths

    >>> found_paths = matches._re_create_file_paths(*matches.get_files().unwrap())
    >>> # [print(found_path) for found_path in found_paths]
    """

    def __init__(self, ft: str = ".nc"):
        self._compset: set[str] = set()
        self._sim: set = set()
        self._ens: set = set()
        self._attr: set = set()
        self._freq: set = set()
        self._date: set = set()
        self._combined: set = set()
        self._bad_files: set[pathlib.Path] = set()
        self.ft = ft
        regex = r"""# Match everything up to "ensemble-simulations"
            .*ensemble-simulations/
            # Match for compset
            # Create a group of as many charaters as you can find that are in a-z or A-Z
            # or _ or -, but stop (?, non-greedy) as soon as another character shows up
            ([a-z,A-Z,0-9,_,-]+?)
            # Look for forward slash and some number of characters, then a -
            /\w+-
            # Match for ensemble
            # Create a group with any number of characters
            (\w+)
            # Match a -
            -
            # Match for simulation type
            # Same group as above, but we do not accept _ this time
            ([a-z,A-Z,0-9,_,-]+?)
            # Match a /, then any number of special or non-special characters, then a /
            /.*/
            # Match for attribute / variable
            # Create a group or some non-zero number of non-special characters
            (\w+)
            # Match a -
            -
            # Match for frequency
            # Create a group of exactly two characters of any type
            (..)
            # Match a -
            -
            # Match for date
            # Match exactly 8 digits
            (\d{8})"""
        pattern = re.compile(regex + self.ft, re.X)
        self.root_path = pathlib.Path(volcano_base.config.DATA_PATH)
        if not self.root_path.exists():
            raise ConnectionError(
                "The file path could not be found. Are you sure the harddisk is"
                " connected?"
            )
        files = self.root_path.rglob(f"**/*{self.ft}")
        self._initial_file_lookup(files, pattern)
        self._matched_files: list[tuple[str, str, str, str, str, str]] | None = None
        self._sort_order: tuple[str, ...] | None = None
        self._sort_reverse: bool = False

    def copy(self) -> Self:
        """Create a shallow copy of this object."""
        # https://stackoverflow.com/a/15774013/10642998
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __len__(self) -> int:
        """Return the number of matched files."""
        if self._matched_files is None:
            raise ValueError("No files have been matched yet.")
        else:
            return len(self._matched_files)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        head = f"{self.__class__.__name__}() contains:"
        files: list[str] = []
        match self.get_files():
            case Success(value):
                files.extend(str(i) for i in value)
            case Failure(value):
                files.append(value)
        return f"{head}\n\t{"\n\t".join(files)}"

    def _initial_file_lookup(self, files, pattern) -> None:
        for file in files:
            if isinstance(search := pattern.search(str(file)), re.Match):
                compset, ens, sim, attr, freq, date = search.groups()
                self._compset.add(compset)
                self._sim.add(sim)
                self._ens.add(ens)
                self._attr.add(attr)
                self._freq.add(freq)
                self._date.add(date)
                self._combined.add((compset, sim, ens, attr, freq, date))
            else:
                self._bad_files.add(file)

    def avail(self) -> None:
        """Print out all available combinations."""
        for h, s_ in zip(
            [
                "Compsets (compset)",
                "Ensembles (ensemble)",
                "Simulations (sim)",
                "Attributes (attr)",
                "Frequencies (freq)",
                "Dates (date)",
            ],
            [
                self._compset,
                self._ens,
                self._sim,
                self._attr,
                self._freq,
                self._date,
            ],
            strict=True,
        ):
            s = sorted(s_)
            print(f"{h}:", end="\r")
            [print(f"\t\t\t{i}") for i in s]

    def get_files(self) -> Result[list[tuple[str, str, str, str, str, str]], str]:
        """Return the list of matched files.

        Returns
        -------
        Result[list[tuple[str, str, str, str, str, str]], str]
            A result type that is a Success or a Failure. Match against it to safely
            obtain the correct output (also see the `print_files()` method)::

                match get_files():
                    case Success(value):
                        [print(v) for v in value]
                    case Failure(value):
                        print(value)
        """
        return (
            Success(self._matched_files)
            if self._matched_files is not None
            else Failure("There are no matched files to return.")
        )

    def print_files(self) -> None:
        """Print all found files if any have been found."""
        match self.get_files():
            case Success(value):
                for i in value:
                    print(i)
            case Failure(value):
                print(value)

    @overload
    def sort(self, *attributes: str, arrays: list[T_Xarray]) -> list[T_Xarray]:
        pass

    @overload
    def sort(self, *attributes: str, reverse: bool) -> Self:
        pass

    @overload
    def sort(self, *attributes: str) -> Self:
        pass

    def sort(
        self,
        *attributes: str,
        arrays: list[T_Xarray] | None = None,
        reverse: bool = False,
    ) -> list[T_Xarray] | Self:
        """Sort a list of arrays based on their attributes.

        Sorting is done such that the first parameter is the most global sorting and the
        last is the most local sorting.

        Parameters
        ----------
        *attributes : str
            Attributes to sort by. The most global sorting is the first parameter, while
            the most local sorting is the last parameter.
        arrays : list[T_Xarray] | None
            An optional list of xarray DataArrays to sort. If None, the matched files
            are used in the sorting.
        reverse : bool
            Reverse the sorting. Default is False.

        Returns
        -------
        list[T_Xarray] | Self
            Returns a list if `arrays` was given, or `self` otherwise
        """
        # We re-set the sort order every time this is called.
        self._sort_order = attributes
        self._sort_reverse = reverse
        if arrays is None and self._matched_files is None:
            return self
        elif arrays is not None:
            return self._sort_xr(arrays, *attributes)
        else:
            return self._sort_tup(*attributes)

    def _sort_xr(self, arrays: list[T_Xarray], *attributes: str) -> list[T_Xarray]:
        """Sort a list of arrays based on their attributes."""
        # Check that the parameters are real attributes of the arrays.
        for a in attributes:
            if any(a not in x.attrs for x in arrays):
                raise AttributeError(
                    "Sorting cannot be done since the parameter is not an attribute of"
                    " all the arrays. Available attributes of the first array are\n"
                    f"{list(arrays[0].attrs.keys())}"
                )

        # Create the sorting key tuple.
        def sorter(x):
            return tuple(x.attrs[attr] for attr in attributes)

        ac = arrays.copy()
        ac.sort(key=sorter, reverse=self._sort_reverse)
        return ac

    def _sort_tup(self, *attributes: str) -> Self:
        """Sort the matched files in the order of their attributes."""
        if self._matched_files is None:
            return self
        # Check that the attributes are valid.
        lookup = {
            "compset": 0,
            "sim": 1,
            "ensemble": 2,
            "attr": 3,
            "freq": 4,
            "date": 5,
        }
        for a in attributes:
            if a not in lookup.keys():
                raise AttributeError(
                    "Sorting cannot be done since the sorting parameter is not an"
                    " attribute of all the arrays. Available attributes are\n"
                    f"{list(lookup.keys())}"
                )

        # Create the sorting key tuple.
        def sorter(x):
            return tuple(x[lookup[attr]] for attr in attributes)

        ac = self._matched_files.copy()
        ac.sort(key=sorter, reverse=self._sort_reverse)
        self._matched_files = ac
        return self

    def find(self, *args: str | Iterable[str]) -> Self:
        """Find files based on groups.

        This does a full new search, and thus resets all previous searches and sorting
        that have been made.

        Parameters
        ----------
        *args : str | Iterable[str]
            Name of a group item or several items that must be found in any given file,
            or an iterable of items that are all part of one group where at least one
            should be found. Run ``self.avail()`` to see all available groups and their
            options.

        Returns
        -------
        Self
            The object itself.

        Raises
        ------
        AttributeError
            If no files were found from the attempted match
        """
        # Unset the sorting.
        self._sort_order = None
        # Single strings in the args list should always be found in 'files', so they
        # must be wrapped in an iterable before we compute the product.
        combinations: list[Iterable[str]] = []
        for elem in args:
            if isinstance(elem, str):
                combinations.append([elem])
            else:  # Maaaybe check in an elif for an instance of an iterable, but nahh
                combinations.append(elem)
        # Find all combinations of the variations of elements we want to find
        prod = list(product(*combinations))
        out: list[tuple[str, str, str, str, str, str]] = []
        for prod_tup in prod:
            if found_tups := [
                tup for tup in self._combined if all(elem in tup for elem in prod_tup)
            ]:
                out.extend(iter(found_tups))
        if out:
            self._matched_files = out
            return self
        err_msg = (
            "I could not find any matches for your search, but here are the individual"
            " sets. Try to specify one at the time, of decreasing importance, to narrow"
            " down what files you have available for your use case."
        )
        raise AttributeError(
            err_msg,
            self._compset,
            self._ens,
            self._sim,
            self._attr,
            self._freq,
            self._date,
        )

    def remove(self, *args: str) -> Self:
        """Remove all files that contain any of the specified groups.

        Parameters
        ----------
        *args : str
            Name of a group that should be removed. Names that refer to the same group
            are accepted, as well as names referring to different groups.

        Returns
        -------
        Self
            The object itself.
        """
        if self._matched_files is None:
            return self
        self._matched_files = [
            tup for tup in self._matched_files if all(elem not in tup for elem in args)
        ]
        # Make sure we keep the sorting order after the refined selection has been make.
        return self if self._sort_order is None else self._sort_tup(*self._sort_order)

    def keep(self, *args: str | Iterable[str]) -> Self:
        """Keep only a subset of the found tuples based on their groups.

        Effectively doing the same as ``self.find``, but on a ``files`` variable
        provided or the already found files instead of on all available files. Useful
        when making several refined selections on already selected files.

        Parameters
        ----------
        *args : str | Iterable[str]
            Name of a group or several groups that must be found in any given file, or
            an iterable of strings that are all part of one group where at least one
            should be found.

        Returns
        -------
        Self
            The object itself.
        """
        if self._matched_files is None:
            return self
        # Single strings in the args list should always be found in 'files', so they
        # must be wrapped in an iterable before we compute the product.
        combinations: list[Iterable[str]] = []
        for elem in args:
            if isinstance(elem, str):
                combinations.append([elem])
            else:  # Maaaybe check in an elif for an instance of an iterable, but nahh
                combinations.append(elem)
        # Find all combinations of the variations of elements we want to find
        prod = list(product(*combinations))
        out: list[tuple[str, str, str, str, str, str]] = []
        for prod_tup in prod:
            if found_tups := [
                tup
                for tup in self._matched_files
                if all(elem in tup for elem in prod_tup)
            ]:
                out.extend(iter(found_tups))
        self._matched_files = out
        # Make sure we keep the sorting order after the refined selection has been made.
        return self if self._sort_order is None else self._sort_tup(*self._sort_order)

    def keep_most_recent(self) -> Self:
        """Keep only the latest file among identical files."""
        if self._matched_files is None:
            return self
        sorting = self._sort_order
        reverse = self._sort_reverse
        self = self.sort(
            "compset", "ensemble", "sim", "attr", "freq", "date", reverse=True
        )
        only_recent = []
        last_file = ("",) * 6
        if self._matched_files is None:
            return self
        for file in self._matched_files:
            if last_file[:-1] != file[:-1]:
                only_recent.append(file)
                last_file = file
        self._matched_files = only_recent
        return self if sorting is None else self.sort(*sorting, reverse=reverse)

    def _re_create_file_paths(
        self,
        *found_files: tuple[str, str, str, str, str, str],
        ft: str | None = None,
        check_existance: bool = True,
    ) -> list[pathlib.Path]:
        """Re-create complete file paths based on tuples made from regex groups.

        Parameters
        ----------
        *found_files : tuple[str, str, str, str, str, str]
            Any number of tuples that were the output of the
            ``self.find`` method.
        ft : str | None
            File type that should be returned. Default is '.nc'.
        check_existance : bool
            Whether to check if the files exists or not

        Returns
        -------
        list[pathlib.Path]
            Files that were re-created and that exists are placed in a list and
            returned.

        Raises
        ------
        FileNotFoundError
            If a file is not found
        """
        if ft is None:
            ft = self.ft
        paths: list[pathlib.Path] = []
        for file_tup in found_files:
            compset, sim, ens, attr, freq, date = file_tup
            path = pathlib.Path(
                self.root_path
                / "ensemble-simulations"
                / compset
                / f"{compset}-{ens}-{sim}"
                / "aggregate"
                / f"{attr}-{freq}-{date}{ft}"
            )
            if not path.exists() and check_existance:
                raise FileNotFoundError(
                    "For some reason, re-creating the file from the regex groups did"
                    " not work! Track this issue down immedeately! The incorrect file"
                    f" path was {path}."
                )
            paths.append(path)
        return paths

    def load(
        self, *files: tuple[str, str, str, str, str, str], ft: str | None = None
    ) -> list[xr.DataArray]:
        """Load files into xr.DataArray objects.

        Parameters
        ----------
        *files : tuple[str, str, str, str, str, str]
            Any number of files, represented as tuples with six elements that uniquely
            specify the file path.
        ft : str | None
            File type that should be returned. Default is '.nc'.

        Returns
        -------
        list[xr.DataArray]
            The same number of objects are returned as was given, but loaded as
            xr.DataArray objects.

        Raises
        ------
        ValueError
            If no files have been matched yet, there is no point in loading
        """
        if ft is None:
            ft = self.ft
        if not files and self._matched_files is None:
            raise ValueError("No files have been matched yet.")
        elif not files and self._matched_files is not None:
            _files = self._matched_files
        elif files:
            _files = list(files)
        xr_arrs: list[xr.DataArray] = []
        for file in _files:
            fp = self._re_create_file_paths(file, ft=ft)[0].resolve()
            xarr = self._open_xr(fp, file) if ft == ".nc" else self._open_np(fp, file)
            file_set = {
                "compset": file[0],
                "sim": file[1],
                "ensemble": file[2],
                "attr": file[3],
                "freq": file[4],
                "date": file[5],
                "file_id": file,
            }
            xarr = xarr.assign_attrs(file_set)
            xr_arrs.append(xarr.chunk({"time": 100}))
        return xr_arrs

    @staticmethod
    def _open_xr(fp, file) -> xr.DataArray:
        xset = xr.open_dataset(fp)
        xarr = getattr(xset, file[3]).assign_attrs(xset.attrs)
        xset.close()
        return xarr

    @staticmethod
    def _open_np(fp, file) -> xr.DataArray:
        with np.load(fp) as f:
            xarr = xr.DataArray(f["data"], dims=["time"], coords={"time": f["times"]})
            file_set = {
                "long_name": volcano_base.config.DATA_ATTRS[file[3]][0],
                "units": volcano_base.config.DATA_ATTRS[file[3]][1],
                "file_id": file,
            }
            xarr = xarr.assign_attrs(file_set)
        return xarr
