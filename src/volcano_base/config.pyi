import pathlib
from _typeshed import Incomplete as Incomplete
from returns.result import Result as Result
from typing import Literal, Never, NoReturn

def never_called(value: Never) -> NoReturn: ...
def ask_then_create(file_path: pathlib.Path) -> None: ...
def create_config() -> Result[pathlib.Path, str]: ...

out: dict[str, dict[str, str]]
PROJECT_ROOT: Incomplete
DATA_PATH: Incomplete
SAVE_PATH: Incomplete
MEANS: dict[Literal['TREFHT'], float]
DATA_ATTRS: Incomplete
