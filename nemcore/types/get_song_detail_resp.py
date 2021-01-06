from typing import List, Any

from .easy_access import EasyAccessDict


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


class Al(EasyAccessDict):
    id: int
    name: str
    pic_url: str
    tns: List[Any]
    pic_str: str
    pic: float


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


class Song(EasyAccessDict):
    name: str
    id: int
    pst: int
    t: int
    ar: List[Ar]
    alia: List[Any]
    pop: int
    st: int
    rt: str
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
    mark: int
    origin_cover_type: int
    origin_song_simple_data: None
    single: int
    no_copyright_rcmd: None
    mv: int
    rtype: int
    rurl: None
    mst: int
    cp: int
    publish_time: int


class GetSongDetailResp(EasyAccessDict):
    songs: List[Song]
    privileges: List[Privilege]
    code: int
