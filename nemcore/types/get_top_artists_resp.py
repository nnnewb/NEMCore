from typing import List, Optional

from .easy_access import EasyAccessDict


class Artist(EasyAccessDict):
    img1_v1_id: float
    topic_person: int
    alias: List[str]
    pic_id: float
    music_size: int
    album_size: int
    brief_desc: str
    followed: bool
    img1_v1_url: str
    trans: str
    pic_url: str
    name: str
    id: int
    account_id: Optional[int]
    pic_id_str: Optional[str]
    img1_v1_id_str: Optional[str]
    trans_names: Optional[List[str]]


class GetTopArtistsResp(EasyAccessDict):
    code: int
    more: bool
    artists: List[Artist]
