from typing import List

from .easy_access import EasyAccessDict


class FreeTrialPrivilege(EasyAccessDict):
    res_consumable: bool
    user_consumable: bool


class Datum(EasyAccessDict):
    id: int
    url: str
    br: int
    size: int
    md5: str
    code: int
    expi: int
    type: str
    gain: int
    fee: int
    uf: None
    payed: int
    flag: int
    can_extend: bool
    free_trial_info: None
    level: str
    encode_type: str
    free_trial_privilege: FreeTrialPrivilege
    url_source: int


class GetSongURLResp(EasyAccessDict):
    data: List[Datum]
    code: int
