from typing import List, Optional, Any

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
    pic_id_str: Optional[str]
    img1_v1_id_str: str


class HotAlbum(EasyAccessDict):
    songs: List[Any]
    paid: bool
    on_sale: bool
    mark: int
    alias: List[str]
    artists: List[Artist]
    copyright_id: int
    pic_id: float
    artist: Artist
    publish_time: int
    company: str
    brief_desc: str
    comment_thread_id: str
    pic: float
    pic_url: str
    company_id: int
    blur_pic_url: str
    tags: str
    description: str
    status: int
    sub_type: str
    name: str
    id: int
    type: str
    size: int
    pic_id_str: Optional[str]
    is_sub: bool


class GetArtistAlbumsResp(EasyAccessDict):
    artist: Artist
    hot_albums: List[HotAlbum]
    more: bool
    code: int
