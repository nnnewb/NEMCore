from pathlib import Path, PurePath
from typing import Union

PathLike = Union[Path, PurePath, str, bytes]


def ensure_path(s) -> Path:
    if not s:
        return s
    return Path(s) if not isinstance(s, Path) else s
