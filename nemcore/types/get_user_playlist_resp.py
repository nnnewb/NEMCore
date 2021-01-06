from typing import List, Any

from .easy_access import EasyAccessDict


class Creator(EasyAccessDict):
    default_avatar: bool
    province: int
    auth_status: int
    followed: bool
    avatar_url: str
    account_status: int
    gender: int
    city: int
    birthday: int
    user_id: int
    user_type: int
    nickname: str
    signature: str
    description: str
    detail_description: str
    avatar_img_id: float
    background_img_id: float
    background_url: str
    authority: int
    mutual: bool
    expert_tags: None
    experts: None
    dj_status: int
    vip_type: int
    remark_name: None
    authentication_types: int
    avatar_detail: None
    anchor: bool
    avatar_img_id_str: str
    background_img_id_str: str
    creator_avatar_img_id_str: str


class Playlist(EasyAccessDict):
    subscribers: List[Any]
    subscribed: bool
    creator: Creator
    artists: None
    tracks: None
    update_frequency: None
    background_cover_id: int
    background_cover_url: None
    title_image: int
    title_image_url: None
    english_title: None
    op_recommend: bool
    recommend_info: None
    ad_type: int
    track_number_update_time: int
    cloud_track_count: int
    subscribed_count: int
    user_id: int
    create_time: int
    high_quality: bool
    update_time: int
    cover_img_id: float
    new_imported: bool
    anonimous: bool
    track_count: int
    total_duration: int
    cover_img_url: str
    special_type: int
    comment_thread_id: str
    privacy: int
    track_update_time: int
    play_count: int
    description: None
    tags: List[Any]
    ordered: bool
    status: int
    name: str
    id: int
    cover_img_id_str: str


class GetUserPlaylistResp(EasyAccessDict):
    version: str
    more: bool
    playlist: List[Playlist]
    code: int
