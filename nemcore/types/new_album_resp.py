from typing import List, Optional, Any

from .easy_access import EasyAccessDict


class Artist(EasyAccessDict):
    img1_v1_id: float
    topic_person: int
    img1_v1_url: str
    music_size: int
    album_size: int
    followed: bool
    brief_desc: str
    trans: str
    pic_url: str
    alias: List[str]
    pic_id: float
    name: str
    id: int
    pic_id_str: Optional[str]
    img1_v1_id_str: str
    trans_names: Optional[List[str]]


class Album(EasyAccessDict):
    songs: List[Any]
    paid: bool
    on_sale: bool
    mark: int
    tags: str
    publish_time: int
    company: str
    comment_thread_id: str
    brief_desc: str
    pic_url: str
    pic: float
    blur_pic_url: str
    company_id: int
    status: int
    sub_type: str
    description: str
    alias: List[str]
    artists: List[Artist]
    copyright_id: int
    pic_id: float
    artist: Artist
    name: str
    id: int
    type: str
    size: int
    pic_id_str: str
    trans_names: Optional[List[str]]


class GetNewAlbumsResp(EasyAccessDict):
    total: int
    albums: List[Album]
    code: int
