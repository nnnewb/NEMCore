import pytest

from nemcore import __version__
from nemcore.netease import NetEase

from logging import getLogger

log = getLogger('nemcore-test')


def test_version():
    assert __version__ == '0.1.2'


@pytest.mark.use_fixtures('cleanup_persistent')
def test_00_login(username, password):
    log.debug(NetEase().login(username, password))


def test_01_get_login_status():
    log.debug(NetEase().get_login_status())


def test_02_login_refresh():
    log.debug(NetEase().login_refresh())


def test_03_get_user_playlist():
    log.debug(NetEase().get_user_playlist())


def test_04_get_recommend_resource():
    log.debug(NetEase().get_recommend_resource())


def test_05_get_recommend_songs():
    log.debug(NetEase().get_recommend_songs())


def test_06_get_personal_fm():
    log.debug(NetEase().get_personal_fm())


@pytest.mark.skip('该操作对账号今后的推荐产生副作用，不进行自动测试')
def test_07_get_personal_fm_like():
    netease = NetEase()
    fm = netease.get_personal_fm()
    log.debug(netease.fm_like(fm['data'][0]['id']))


@pytest.mark.skip('该操作对账号今后的推荐产生副作用，不进行自动测试')
def test_08_get_personal_fm_trash():
    netease = NetEase()
    fm = netease.get_personal_fm()
    log.debug(netease.fm_trash(fm['data'][0]['id']))


def test_09_search():
    log.debug(NetEase().search('戦姫絶唱'))


def test_10_get_new_albums():
    log.debug(NetEase().get_new_albums())


def test_11_get_top_playlists():
    log.debug(NetEase().get_top_playlists())


def test_12_catalogs():
    log.debug(NetEase().playlist_catelogs())


def test_13_playlist_detail():
    top = NetEase().get_top_playlists()
    log.debug(NetEase().get_playlist_detail(top['playlists'][0]['id']))


def test_14_top_artists():
    log.debug(NetEase().get_top_artists())


def test_15_top_songs():
    log.debug(NetEase().get_top_songs(0))


def test_16_get_artist_info():
    netease = NetEase()
    artists = netease.get_top_artists()
    log.debug(NetEase().get_artist_info(artists['artists'][0]['id']))


def test_17_get_artist_albums():
    netease = NetEase()
    artists = netease.get_top_artists()
    log.debug(NetEase().get_artist_albums(artists['artists'][0]['id']))


def test_18_get_album_info():
    netease = NetEase()
    artists = netease.get_top_artists()
    albums = netease.get_artist_albums(artists['artists'][0]['id'])
    log.debug(netease.get_album_info(albums['hotAlbums'][0]['id']))


def test_19_get_song_comments():
    netease = NetEase()
    songs = netease.get_top_songs(0)
    log.debug(netease.get_song_comments(songs['playlist']['tracks'][0]['id']))


def test_20_get_songs_detail():
    netease = NetEase()
    songs = netease.get_top_songs(0)
    log.debug(netease.get_songs_detail([songs['playlist']['tracks'][0]['id']]))


def test_21_get_songs_url():
    netease = NetEase()
    songs = netease.get_top_songs(0)
    log.debug(netease.get_songs_url([songs['playlist']['tracks'][0]['id']], 0))


def test_22_get_song_lyric():
    netease = NetEase()
    songs = netease.get_top_songs(0)
    log.debug(netease.get_song_lyric(songs['playlist']['tracks'][0]['id']))


def test_23_get_djchannels():
    log.debug(NetEase().get_djchannels())


def test_24_get_djprograms():
    channels = NetEase().get_djchannels()
    log.debug(NetEase().get_djprograms(channels['djRadios'][0]['id']))


@pytest.mark.skip('签到每天只能执行一次，不适合自动测试')
def test_98_daily_task():
    netease = NetEase()
    netease.daily_task()
