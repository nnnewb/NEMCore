from typing import List, Optional, Any

from .easy_access import EasyAccessDict


class Artist(EasyAccessDict):
    img1_v1_id: float
    topic_person: int
    alias: List[str]
    pic_id: float
    pic_url: str
    brief_desc: str
    music_size: int
    album_size: int
    followed: bool
    img1_v1_url: str
    trans: str
    name: str
    id: int
    pic_id_str: Optional[str]
    img1_v1_id_str: str


class ResourceInfo(EasyAccessDict):
    id: int
    user_id: int
    name: str
    img_url: str
    creator: None
    encoded_id: None
    sub_title: None
    web_url: None


class CommentThread(EasyAccessDict):
    id: str
    resource_info: ResourceInfo
    resource_type: int
    comment_count: int
    liked_count: int
    share_count: int
    hot_count: int
    latest_liked_users: None
    resource_id: int
    resource_owner_id: int
    resource_title: str


class Info(EasyAccessDict):
    comment_thread: CommentThread
    latest_liked_users: None
    liked: bool
    comments: None
    resource_type: int
    resource_id: int
    comment_count: int
    liked_count: int
    share_count: int
    thread_id: str


class Album(EasyAccessDict):
    songs: List[Any]
    paid: bool
    on_sale: bool
    mark: int
    description: str
    status: int
    tags: str
    alias: List[Any]
    artists: List[Artist]
    copyright_id: int
    pic_id: float
    artist: Artist
    pic_url: str
    company: str
    brief_desc: str
    publish_time: int
    comment_thread_id: str
    pic: float
    blur_pic_url: str
    company_id: int
    sub_type: str
    name: str
    id: int
    type: str
    size: int
    pic_id_str: str
    info: Info


class Al(EasyAccessDict):
    id: int
    name: str
    pic_url: str
    pic_str: str
    pic: float


class Ar(EasyAccessDict):
    id: int
    name: str
    alia: Optional[List[str]]


class H(EasyAccessDict):
    br: int
    fid: int
    size: int
    vd: int


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


class Song(EasyAccessDict):
    rt_urls: List[Any]
    ar: List[Ar]
    al: Al
    st: int
    no_copyright_rcmd: None
    no: int
    fee: int
    dj_id: int
    v: int
    mv: int
    cd: str
    a: None
    m: H
    h: H
    l: H
    rt_url: None
    ftype: int
    rtype: int
    rurl: None
    pst: int
    t: int
    alia: List[str]
    pop: int
    rt: str
    mst: int
    cp: int
    crbt: None
    cf: str
    dt: int
    name: str
    id: int
    privilege: Privilege


class GetAlbumInfoResp(EasyAccessDict):
    songs: List[Song]
    code: int
    album: Album
