from typing import List, Any

from .easy_access import EasyAccessDict


class FMTrashResp(EasyAccessDict):
    songs: List[Any]
    count: int
    code: int
