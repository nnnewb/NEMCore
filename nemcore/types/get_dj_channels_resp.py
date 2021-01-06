from typing import Optional, List, Dict

from .easy_access import EasyAccessDict


class Dj(EasyAccessDict):
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
    avatar_detail: None
    anchor: bool
    background_img_id_str: str
    avatar_img_id_str: str
    dj_avatar_img_id_str: Optional[str]


class DjRadio(EasyAccessDict):
    id: int
    name: str
    pic_url: str
    program_count: int
    sub_count: int
    create_time: int
    category_id: int
    category: str
    rcmdtext: Optional[str]
    radio_fee_type: int
    fee_scope: int
    play_count: int
    subed: bool
    dj: Dj
    copywriter: Optional[str]
    buyed: bool


class GetDjChannelsResp(EasyAccessDict):
    dj_radios: List[DjRadio]
    has_more: bool
    code: int
