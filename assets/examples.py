"""Script showing example usage of the package."""

import volcano_base


def _main() -> None:
    # ff = volcano_base.load.FindFiles(regex=volcano_base.load.nird_archive_regex())
    ff = volcano_base.load.FindFiles()
    ff.avail()
    ff.find("strong", "ens2", "h0")
    cp: volcano_base.load.FindFiles = ff.copy()
    ff.remove("FLNT", "e_BWma1850")
    ff.keep("FSNT")
    cp.sort("attr")
    cp.remove("TMso4_a2")
    print(ff, "\n", len(ff))
    print(cp, "\n", len(cp))
    cp = cp.keep_most_recent()
    print(cp, "\n", len(cp))
    print(ff.get_files().unwrap())
    found_paths = ff._re_create_file_paths(*ff.get_files().unwrap())
    [print(found_path) for found_path in found_paths]
    file = ff.load()
    print(file)


if __name__ == "__main__":
    _main()
