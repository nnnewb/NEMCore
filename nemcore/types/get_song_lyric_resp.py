from .easy_access import EasyAccessDict


class Klyric(EasyAccessDict):
    version: int
    lyric: str


class GetSongLyricResp(EasyAccessDict):
    sgc: bool
    sfy: bool
    qfy: bool
    lrc: Klyric
    klyric: Klyric
    tlyric: Klyric
    code: int
