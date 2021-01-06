from typing import List, Optional, Any

from .easy_access import EasyAccessDict


class Artist(EasyAccessDict):
    img1_v1_id: float
    topic_person: int
    alias: List[str]
    pic_id: float
    brief_desc: str
    music_size: int
    album_size: int
    followed: bool
    img1_v1_url: str
    trans: str
    pic_url: str
    name: str
    id: int
    publish_time: int
    account_id: int
    pic_id_str: str
    img1_v1_id_str: str
    mv_size: int


class Al(EasyAccessDict):
    id: int
    name: str
    pic_url: str
    pic_str: str
    pic: float
    alia: Optional[List[str]]


class Ar(EasyAccessDict):
    id: int
    name: str
    alia: Optional[List[str]]


class H(EasyAccessDict):
    br: int
    fid: int
    size: int
    vd: float


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


class HotSong(EasyAccessDict):
    rt_urls: List[Any]
    ar: List[Ar]
    al: Al
    st: int
    no_copyright_rcmd: None
    dj_id: int
    no: int
    fee: int
    v: int
    mv: int
    cd: str
    rtype: int
    rurl: None
    pst: int
    t: int
    alia: List[str]
    pop: int
    rt: Optional[str]
    mst: int
    cp: int
    crbt: None
    cf: str
    dt: int
    h: H
    l: H
    rt_url: None
    ftype: int
    a: None
    m: Optional[H]
    name: str
    id: int
    privilege: Privilege
    eq: Optional[str]


class GetArtistInfoResp(EasyAccessDict):
    artist: Artist
    hot_songs: List[HotSong]
    more: bool
    code: int
