from typing import List, Any, Optional

from nemcore.types.easy_access import EasyAccessDict


class Artist(EasyAccessDict):
    id: int
    name: str
    pic_url: None
    alias: List[Any]
    album_size: int
    pic_id: int
    img1_v1_url: str
    img1_v1: int
    trans: None


class Album(EasyAccessDict):
    id: int
    name: str
    artist: Artist
    publish_time: int
    size: int
    copyright_id: int
    status: int
    pic_id: float
    mark: int
    trans_names: Optional[List[str]]
    alia: Optional[List[str]]


class Song(EasyAccessDict):
    id: int
    name: str
    artists: List[Artist]
    album: Album
    duration: int
    copyright_id: int
    status: int
    alias: List[str]
    rtype: int
    ftype: int
    mvid: int
    fee: int
    r_url: None
    mark: float


class Result(EasyAccessDict):
    songs: List[Song]
    has_more: bool
    song_count: int


class SearchResp(EasyAccessDict):
    result: Result
    code: int
