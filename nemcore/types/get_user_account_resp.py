from nemcore.types.easy_access import EasyAccessDict


class Account(EasyAccessDict):
    id: int
    user_name: str
    type: int
    status: int
    whitelist_authority: int
    create_time: int
    token_version: int
    ban: int
    baoyue_version: int
    donate_version: int
    vip_type: int
    anonimous_user: bool
    paid_fee: bool


class Profile(EasyAccessDict):
    user_id: int
    user_type: int
    nickname: str
    avatar_img_id: float
    avatar_url: str
    background_img_id: float
    background_url: str
    signature: None
    create_time: int
    user_name: str
    account_type: int
    short_user_name: str
    birthday: int
    authority: int
    gender: int
    account_status: int
    province: int
    city: int
    auth_status: int
    description: None
    detail_description: None
    default_avatar: bool
    expert_tags: None
    experts: None
    dj_status: int
    location_status: int
    vip_type: int
    followed: bool
    mutual: bool
    authenticated: bool
    last_login_time: int
    last_login_ip: str
    remark_name: None
    viptype_version: int
    authentication_types: int
    avatar_detail: None
    anchor: bool


class GetUserAccountResp(EasyAccessDict):
    code: int
    account: Account
    profile: Profile
