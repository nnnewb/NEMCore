from typing import List

from .easy_access import EasyAccessDict


class Account(EasyAccessDict):
    id: int
    user_name: str
    type: int
    status: int
    whitelist_authority: int
    create_time: int
    salt: str
    token_version: int
    ban: int
    baoyue_version: int
    donate_version: int
    vip_type: int
    viptype_version: int
    anonimous_user: bool


class Binding(EasyAccessDict):
    refresh_time: int
    binding_time: int
    expired: bool
    url: str
    user_id: int
    token_json_str: str
    expires_in: int
    id: int
    type: int


class Experts(EasyAccessDict):
    pass


class Profile(EasyAccessDict):
    followed: bool
    background_url: str
    detail_description: str
    background_img_id_str: str
    avatar_img_id_str: str
    description: str
    user_id: int
    user_type: int
    mutual: bool
    remark_name: None
    expert_tags: None
    auth_status: int
    experts: Experts
    vip_type: int
    gender: int
    account_status: int
    avatar_img_id: float
    nickname: str
    birthday: int
    city: int
    background_img_id: float
    avatar_url: str
    default_avatar: bool
    province: int
    dj_status: int
    signature: str
    authority: int
    profile_avatar_img_id_str: str
    followeds: int
    follows: int
    event_count: int
    avatar_detail: None
    playlist_count: int
    playlist_be_subscribed_count: int


class LoginResp(EasyAccessDict):
    login_type: int
    code: int
    account: Account
    token: str
    profile: Profile
    bindings: List[Binding]
