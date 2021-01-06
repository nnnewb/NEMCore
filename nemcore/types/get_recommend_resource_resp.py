from typing import Optional, List

from .easy_access import EasyAccessDict


class Creator(EasyAccessDict):
    remark_name: None
    mutual: bool
    background_url: str
    detail_description: str
    default_avatar: bool
    expert_tags: Optional[List[str]]
    dj_status: int
    followed: bool
    avatar_img_id: float
    background_img_id: float
    avatar_img_id_str: str
    background_img_id_str: str
    user_id: int
    account_status: int
    vip_type: int
    province: int
    avatar_url: str
    auth_status: int
    user_type: int
    nickname: str
    gender: int
    birthday: int
    city: int
    description: str
    signature: str
    authority: int


class Recommend(EasyAccessDict):
    id: int
    type: int
    name: str
    copywriter: str
    pic_url: str
    playcount: int
    create_time: int
    creator: Creator
    track_count: int
    user_id: int
    alg: str


class GetRecommendResourceResp(EasyAccessDict):
    code: int
    feature_first: bool
    have_rcmd_songs: bool
    recommend: List[Recommend]
