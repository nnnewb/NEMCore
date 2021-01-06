from typing import List, Any

from .easy_access import EasyAccessDict


class FMLikeResp(EasyAccessDict):
    songs: List[Any]
    playlist_id: int
    code: int
