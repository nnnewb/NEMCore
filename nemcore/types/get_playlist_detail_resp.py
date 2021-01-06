from typing import List, Optional, Any

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


class TrackID(EasyAccessDict):
    id: int
    v: int
    at: int
    alg: None


class Al(EasyAccessDict):
    id: int
    name: str
    pic_url: str
    tns: List[str]
    pic: float
    pic_str: Optional[str]


class Ar(EasyAccessDict):
    id: int
    name: str
    tns: List[Any]
    alias: List[Any]


class H(EasyAccessDict):
    br: int
    fid: int
    size: int
    vd: int


class Track(EasyAccessDict):
    name: str
    id: int
    pst: int
    t: int
    ar: List[Ar]
    alia: List[str]
    pop: int
    st: int
    rt: Optional[str]
    fee: int
    v: int
    crbt: None
    cf: str
    al: Al
    dt: int
    h: H
    m: H
    l: H
    a: None
    cd: str
    no: int
    rt_url: None
    ftype: int
    rt_urls: List[Any]
    dj_id: int
    copyright: int
    s_id: int
    mark: float
    origin_cover_type: int
    origin_song_simple_data: None
    single: int
    no_copyright_rcmd: None
    mst: int
    cp: int
    mv: int
    rtype: int
    rurl: None
    publish_time: int


class Playlist(EasyAccessDict):
    subscribers: List[Any]
    subscribed: bool
    creator: Creator
    tracks: List[Track]
    video_ids: None
    videos: None
    track_ids: List[TrackID]
    update_frequency: None
    background_cover_id: int
    background_cover_url: None
    title_image: int
    title_image_url: None
    english_title: None
    op_recommend: bool
    subscribed_count: int
    cloud_track_count: int
    user_id: int
    track_number_update_time: int
    create_time: int
    high_quality: bool
    cover_img_id: float
    track_count: int
    new_imported: bool
    cover_img_url: str
    special_type: int
    update_time: int
    comment_thread_id: str
    track_update_time: int
    privacy: int
    play_count: int
    ad_type: int
    ordered: bool
    tags: List[Any]
    description: None
    status: int
    name: str
    id: int
    share_count: int
    cover_img_id_str: str
    comment_count: int


class ChargeInfoList(EasyAccessDict):
    rate: int
    charge_url: None
    charge_message: None
    charge_type: int


class FreeTrialPrivilege(EasyAccessDict):
    res_consumable: bool
    user_consumable: bool


class Privilege(EasyAccessDict):
    id: int
    fee: int
    payed: int
    st: int
    pl: int
    dl: int
    sp: int
    cp: int
    subp: int
    cs: bool
    maxbr: int
    fl: int
    toast: bool
    flag: int
    pre_sell: bool
    play_maxbr: int
    download_maxbr: int
    free_trial_privilege: FreeTrialPrivilege
    charge_info_list: List[ChargeInfoList]


class GetPlaylistDetailResp(EasyAccessDict):
    code: int
    related_videos: None
    playlist: Playlist
    urls: None
    privileges: List[Privilege]
