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


class CESM2FileNotFound(FileNotFoundError):
    """Raise an error if one of the CESM2 files are not found."""

    def __init__(self, *args: object) -> None:
        file = volcano_base.config.DATA_PATH
        msg = (
            f'Cannot find the file "{args[0]}", which is a necessary CESM2 file.'
            if args
            else "Cannot find the necessary CESM2 files."
        )
        self.message = f"{msg} I went looking in {file.resolve()}. Please run the `save_cesm_files` function within `down.cesm2` to see what files are missing."
        super().__init__(self.message)


class RegexLookup:
    """Create a regex for the files you want to find with FindFiles.

    Parameters
    ----------
    ft : str
        File type that should be found. Default is '.nc'.
    group_names : dict[str, str]
        Dictionary with the group names and the corresponding regex group names.
    reverse_search_query : pathlib.Path
        Path to the file that should be found using the regex groups.
    regex : str
        Regular expression that should be used to find the files.

    Raises
    ------
    CESM2FileNotFound
        If the files cannot be found the hard disk might not be mounted
    """

    def __init__(
        self,
        ft: str,
        group_names: dict[str, str],
        reverse_search_query: pathlib.Path,
        regex: str,
    ) -> None:
        self.ft = ft if ft.startswith(".") else f".{ft}"
        for name in group_names.values():
            name_ = f"<{name}>"
            if name_ not in str(reverse_search_query.resolve()):
                raise ValueError(
                    "The reverse_search must contain all group_name values and the file type ft."
                )
            setattr(self, f"_{name}", set())
        self.groups = group_names
        self.reverse_search_query = reverse_search_query
        self.regex = regex
        self._combined: set = set()
        self._bad_files: set[pathlib.Path] = set()

    def search(self) -> None:
        """Search for files in the root path that match the regular expression."""
        pattern = re.compile(self.regex + self.ft, re.X)
        self.root_path = volcano_base.config.DATA_PATH
        if not self.root_path.exists():
            raise CESM2FileNotFound()
        files = self.root_path.rglob(f"**/*{self.ft}")
        self._initial_file_lookup(files, pattern)

    def reverse_search(self, file_tuple: tuple[str, ...], ft: str) -> pathlib.Path:
        """Look for file paths using the regex match groups."""
        # Substitute all instances of group values in the reverse search string
        this_search = self.reverse_search_query
        for i, v in enumerate(file_tuple):
            this_search = pathlib.Path(
                str(this_search).replace(f"<{list(self.groups.values())[i]}>", v)
            )
        this_search = pathlib.Path(str(this_search).replace("<ft>", ft))
        return self.root_path / this_search

    def _initial_file_lookup(self, files, pattern) -> None:
        for file in files:
            if isinstance(search := pattern.search(str(file)), re.Match):
                for i, v in enumerate(search.groups()):
                    getattr(self, f"_{list(self.groups.values())[i]}").add(v)
                self._combined.add(tuple(search.groups()))
            else:
                self._bad_files.add(file)


def default_regex() -> RegexLookup:
    """Return a regex object that looks for files using the initial directory hierarchy."""
    regex = r"""# Match everything up to "ensemble-simulations"
        .*ensemble-simulations/
        # Match for compset (group 1)
        # Create a group of as many characters as you can find that are in a-z or A-Z
        # or _ or -, but stop (?, non-greedy) as soon as another character shows up
        ([a-z,A-Z,0-9,_,-]+?)
        # Look for forward slash and some number of characters, then a -
        /\w+-
        # Match for ensemble (group 2)
        # Create a group with any number of characters
        (\w+)
        # Match a -
        -
        # Match for simulation type (group 3)
        # Same group as above
        ([a-z,A-Z,0-9,_,-]+?)
        # Match a /, then any number of special or non-special characters, then a /
        /.*/
        # Match for attribute / variable (group 4)
        # Create a group of some non-zero number of non-special characters
        (\w+)
        # Match a -
        -
        # Match for frequency (group 5)
        # Create a group of exactly two characters of any type
        (..)
        # Match a -
        -
        # Match for date (group 6)
        # Match exactly 8 digits
        (\d{8})"""
    group_names = {
        "Compsets": "compset",
        "Ensembles": "ensemble",
        "Simulations": "sim",
        "Attributes": "attr",
        "Frequencies": "freq",
        "Dates": "date",
    }
    reverse_search = (
        pathlib.Path("ensemble-simulations")
        / "<compset>"
        / "<compset>-<ensemble>-<sim>"
        / "aggregate"
        / "<attr>-<freq>-<date><ft>"
    )
    return RegexLookup(".nc", group_names, reverse_search, regex)


def nird_archive_regex() -> RegexLookup:
    """Return a regex object that looks for files using the NIRD archive directory hierarchy."""
    regex = r"""# Match everything up to "nird-archive"
        .*nird-archive/
        (.*)
        -
        (.*)
        -
        (.*)
        -
        (.*)
        -
        (.*)
        -
        (.*)
        -
        (\d{8})"""
    group_names = {
        "Compsets": "compset",
        "Latutude": "latitude",
        "Simulations": "sim",
        "Ensembles": "ensemble",
        "Attributes": "attr",
        "Frequencies": "freq",
        "Dates": "date",
    }
    reverse_search = (
        pathlib.Path("nird-archive")
        / "<compset>-<latitude>-<sim>-<ensemble>-<attr>-<freq>-<date><ft>"
    )
    return RegexLookup(".nc", group_names, reverse_search, regex)


class FindFiles:
    """Find files that match a pre-defined regular expression.

    Parameters
    ----------
    regex : RegexLookup | None
        A RegexLookup object that contains the regular expression and the groups that
        should be found.

    Attributes
    ----------
    _matched_files : files that have been looked up among the files found with the regex
    _sort_order : tuple with the sorting that is applied to the files
    _sort_reverse : bool stating if the sorting of the files should be reversed

    Examples
    --------
    >>> ff = FindFiles()

    You find nothing since the date is wrong.

    >>> files = ff.find("h0", "e_BWma1850", "strong", "U", "ens1", "2x230828")
    Traceback (most recent call last):
    ...
    AttributeError: ...
    >>> # [print(m) for m in files.get_files()]

    You still find nothing since there are two specifications of ensembles.

    >>> files = ff.find("h0", "e_BWma1850", "strong", "U", "ens1", "ens2")
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
    ...     "h0",
    ...     ("e_BWma1850", "e_fSST1850"),
    ...     ["FLNT", "TREFHT", "AODVISstdn"],
    ...     {"ens1", "ens2"},
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

    def __init__(self, regex: RegexLookup | None = None):
        self.regex = default_regex() if regex is None else regex
        self.regex.search()
        self._matched_files: list[tuple[str, ...]] | None = None
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

    def avail(self) -> None:
        """Print out all available combinations."""
        dict_list = [f"{key} ({value})" for key, value in self.regex.groups.items()]
        longest = max(len(i) + 1 for i in dict_list) // 8 + 1
        for h, s_ in zip(
            dict_list,
            [getattr(self.regex, f"_{name}") for name in self.regex.groups.values()],
            strict=True,
        ):
            s = sorted(s_)
            print(f"{h}:", end="\r")
            tab = "\t" * longest
            [print(f"{tab}{i}") for i in s]

    def get_files(self) -> Result[list[tuple[str, ...]], str]:
        """Return the list of matched files.

        Returns
        -------
        Result[list[tuple[str, ...]], str]
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
        lookup = {v: i for i, v in enumerate(self.regex.groups.values())}
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
        out: list[tuple[str, ...]] = []
        for prod_tup in prod:
            if found_tups := [
                tup
                for tup in self.regex._combined
                if all(elem in tup for elem in prod_tup)
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
            *[getattr(self.regex, f"_{name}") for name in self.regex.groups.values()],
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
        out: list[tuple[str, ...]] = []
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
        """Keep only the latest file among identical files.

        This assumes that there is a sorting attribute named 'date' that is available.
        """
        if self._matched_files is None:
            return self
        sorting = self._sort_order
        reverse = self._sort_reverse
        local_self = self.sort("date", reverse=True)
        only_recent: list[tuple[str, ...]] = []
        if local_self._matched_files is None:
            return self
        for file in local_self._matched_files:
            tuple_exists = any(
                file[:-1] == existing_tuple[:-1] for existing_tuple in only_recent
            )
            if not tuple_exists or not only_recent:
                only_recent.append(file)
        local_self._matched_files = only_recent
        return (
            local_self
            if sorting is None
            else local_self.sort(*sorting, reverse=reverse)
        )

    def _re_create_file_paths(
        self,
        *found_files: tuple[str, ...],
        ft: str | None = None,
        check_existence: bool = True,
    ) -> list[pathlib.Path]:
        """Re-create complete file paths based on tuples made from regex groups.

        Parameters
        ----------
        *found_files : tuple[str, ...]
            Any number of tuples that were the output of the
            ``self.find`` method.
        ft : str | None
            File type that should be returned. Default is to use the file type of the
            regex object.
        check_existence : bool
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
            ft = self.regex.ft
        paths: list[pathlib.Path] = []
        for file_tup in found_files:
            path = self.regex.reverse_search(file_tup, ft)
            if not path.exists() and check_existence:
                raise FileNotFoundError(
                    "For some reason, re-creating the file from the regex groups did"
                    " not work! Track this issue down immediately! The incorrect file"
                    f" path was '{path}'."
                )
            paths.append(path)
        return paths

    def load(
        self, *files: tuple[str, ...], ft: str | None = None
    ) -> list[xr.DataArray]:
        """Load files into xr.DataArray objects.

        Parameters
        ----------
        *files : tuple[str, ...]
            Any number of files, represented as tuples with six elements that uniquely
            specify the file path.
        ft : str | None
            File type that should be returned. Default is to use the file type of the
            regex object.

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
            ft = self.regex.ft
        match files, self._matched_files:
            case ([], None):
                raise ValueError("No files have been matched yet.")
            case ([], list(match_files)):
                _files = match_files
            case (files, _):
                _files = list(files)
        xr_arrs: list[xr.DataArray] = []
        for file in _files:
            attr_idx = list(self.regex.groups.values()).index("attr")
            attr = file[attr_idx]
            fp = self._re_create_file_paths(file, ft=ft)[0].resolve()
            xarr = (
                self._open_xr(fp, attr)
                if ft == ".nc"
                else self._open_np(fp, file, attr)
            )
            file_set = {v: file[i] for i, v in enumerate(self.regex.groups.values())}
            file_set["file_id"] = str(file)
            xarr = xarr.assign_attrs(file_set)
            if "time" in xarr.dims:
                xr_arrs.append(xarr.chunk({"time": 100}))
            else:
                xr_arrs.append(xarr)
        return xr_arrs

    @staticmethod
    def _open_xr(fp, file) -> xr.DataArray:
        xset = xr.open_dataset(fp)
        xarr = getattr(xset, file).assign_attrs(xset.attrs)
        xset.close()
        return xarr

    @staticmethod
    def _open_np(fp, file, attr) -> xr.DataArray:
        with np.load(fp) as f:
            xarr = xr.DataArray(f["data"], dims=["time"], coords={"time": f["times"]})
            file_set = {
                "long_name": volcano_base.config.DATA_ATTRS[attr][0],
                "units": volcano_base.config.DATA_ATTRS[attr][1],
                "file_id": file,
            }
            xarr = xarr.assign_attrs(file_set)
        return xarr
