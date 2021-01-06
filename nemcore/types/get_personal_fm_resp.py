from typing import List, Any, Optional

from nemcore.types.easy_access import EasyAccessDict


class Artist(EasyAccessDict):
    name: str
    id: int
    pic_id: int
    img1_v1_id: int
    brief_desc: str
    pic_url: str
    img1_v1_url: str
    album_size: int
    alias: List[Any]
    trans: str
    music_size: int
    topic_person: int


class Album(EasyAccessDict):
    name: str
    id: int
    type: str
    size: int
    pic_id: float
    blur_pic_url: str
    company_id: int
    pic: float
    pic_url: str
    publish_time: int
    description: str
    tags: str
    company: str
    brief_desc: str
    artist: Artist
    songs: List[Any]
    alias: List[str]
    status: int
    copyright_id: int
    comment_thread_id: str
    artists: List[Artist]
    sub_type: str
    trans_name: None
    on_sale: bool
    mark: int
    pic_id_str: Optional[str]


class Music(EasyAccessDict):
    name: None
    id: int
    size: int
    extension: str
    sr: int
    dfs_id: int
    bitrate: int
    play_time: int
    volume_delta: int


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


class Datum(EasyAccessDict):
    name: str
    id: int
    position: int
    alias: List[str]
    status: int
    fee: int
    copyright_id: int
    disc: int
    no: int
    artists: List[Artist]
    album: Album
    starred: bool
    popularity: int
    score: int
    starred_num: int
    duration: int
    played_num: int
    day_plays: int
    hear_time: int
    ringtone: str
    crbt: None
    audition: None
    copy_from: str
    comment_thread_id: str
    rt_url: None
    ftype: int
    rt_urls: List[Any]
    copyright: int
    trans_name: None
    sign: None
    mark: int
    origin_cover_type: int
    origin_song_simple_data: None
    single: int
    no_copyright_rcmd: None
    rtype: int
    rurl: None
    mvid: int
    b_music: Music
    mp3_url: None
    l_music: Music
    h_music: Music
    m_music: Music
    privilege: Privilege
    alg: str


class GetPersonalFMResp(EasyAccessDict):
    pop_adjust: bool
    data: List[Datum]
    code: int
