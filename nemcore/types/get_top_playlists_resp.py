from typing import Optional, List, Dict

from .easy_access import EasyAccessDict


class AvatarDetail(EasyAccessDict):
    user_type: int
    identity_level: int
    identity_icon_url: str


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
    expert_tags: Optional[List[str]]
    experts: Optional[Dict[str, str]]
    dj_status: int
    vip_type: int
    remark_name: None
    authentication_types: int
    avatar_detail: Optional[AvatarDetail]
    anchor: bool
    background_img_id_str: str
    avatar_img_id_str: str
    creator_avatar_img_id_str: Optional[str]


class Playlist(EasyAccessDict):
    name: str
    id: int
    track_number_update_time: int
    status: int
    user_id: int
    create_time: int
    update_time: int
    subscribed_count: int
    track_count: int
    cloud_track_count: int
    cover_img_url: str
    cover_img_id: float
    description: str
    tags: List[str]
    play_count: int
    track_update_time: int
    special_type: int
    total_duration: int
    creator: Creator
    tracks: None
    subscribers: List[Creator]
    subscribed: bool
    comment_thread_id: str
    new_imported: bool
    ad_type: int
    high_quality: bool
    privacy: int
    ordered: bool
    anonimous: bool
    cover_status: int
    recommend_info: None
    share_count: int
    cover_img_id_str: str
    comment_count: int
    alg: str


class GetTopPlaylistsResp(EasyAccessDict):
    playlists: List[Playlist]
    total: int
    code: int
    more: bool
    cat: str
