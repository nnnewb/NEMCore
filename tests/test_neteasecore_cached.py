import pytest

from nemcore.api import NetEaseApi

from logging import getLogger
import os

log = getLogger('nemcore-test')
log.setLevel('DEBUG')


@pytest.fixture()
def netease(mocker):
    netease = NetEaseApi()
    netease.setup_cache()
    mocker.patch.object(netease,
                        '_raw_request',
                        autospec=True,
                        side_effect=netease._raw_request)

    yield netease


@pytest.mark.skip('需要登录')
def test_00_login(username, password):
    log.debug(netease.login(username, password))


def test_01_get_login_status(netease, mocker):
    log.debug(netease.get_login_status())
    log.debug(netease.get_login_status())

    assert netease._raw_request.call_count == 2


def test_02_login_refresh(netease):
    log.debug(netease.login_refresh())
    log.debug(netease.login_refresh())

    assert netease._raw_request.call_count == 2


@pytest.mark.skip('需要登陆')
def test_03_get_user_playlist(netease):
    log.debug(netease.get_user_playlist())
    log.debug(netease.get_user_playlist())

    assert netease._raw_request.call_count == 1


@pytest.mark.skip('需要登陆')
def test_04_get_recommend_resource(netease):
    log.debug(netease.get_recommend_resource())
    log.debug(netease.get_recommend_resource())

    assert netease._raw_request.call_count == 1


@pytest.mark.skip('需要登陆')
def test_05_get_recommend_songs(netease):
    log.debug(netease.get_recommend_songs())
    log.debug(netease.get_recommend_songs())

    assert netease._raw_request.call_count == 1


def test_06_get_personal_fm(netease):
    log.debug(netease.get_personal_fm())
    log.debug(netease.get_personal_fm())

    assert netease._raw_request.call_count == 1


@pytest.mark.skip('该操作对账号今后的推荐产生副作用，不进行自动测试')
def test_07_get_personal_fm_like(netease):
    fm = netease.get_personal_fm()
    log.debug(netease.fm_like(fm['data'][0]['id']))
    log.debug(netease.fm_like(fm['data'][0]['id']))

    assert netease._raw_request.call_count == 2


@pytest.mark.skip('该操作对账号今后的推荐产生副作用，不进行自动测试')
def test_08_get_personal_fm_trash(netease):
    fm = netease.get_personal_fm()
    log.debug(netease.fm_trash(fm['data'][0]['id']))
    log.debug(netease.fm_trash(fm['data'][0]['id']))

    assert netease._raw_request.call_count == 2


def test_09_search(netease):
    log.debug(netease.search('戦姫絶唱'))
    log.debug(netease.search('戦姫絶唱'))

    assert netease._raw_request.call_count == 1


def test_10_get_new_albums(netease):
    log.debug(netease.get_new_albums())
    log.debug(netease.get_new_albums())

    assert netease._raw_request.call_count == 1


def test_11_get_top_playlists(netease):
    log.debug(netease.get_top_playlists())
    log.debug(netease.get_top_playlists())

    assert netease._raw_request.call_count == 1


def test_12_catalogs(netease):
    log.debug(netease.playlist_catelogs())
    log.debug(netease.playlist_catelogs())

    assert netease._raw_request.call_count == 1


def test_13_playlist_detail(netease):
    top = netease.get_top_playlists()
    log.debug(netease.get_playlist_detail(top['playlists'][0]['id']))
    log.debug(netease.get_playlist_detail(top['playlists'][0]['id']))

    assert netease._raw_request.call_count == 2


def test_14_top_artists(netease):
    log.debug(netease.get_top_artists())
    log.debug(netease.get_top_artists())

    assert netease._raw_request.call_count == 1


def test_15_top_songs(netease):
    log.debug(netease.get_top_songs(0))
    log.debug(netease.get_top_songs(0))

    assert netease._raw_request.call_count == 1


def test_16_get_artist_info(netease):
    artists = netease.get_top_artists()
    log.debug(netease.get_artist_info(artists['artists'][0]['id']))
    log.debug(netease.get_artist_info(artists['artists'][0]['id']))

    assert netease._raw_request.call_count == 2


def test_17_get_artist_albums(netease):
    artists = netease.get_top_artists()
    log.debug(netease.get_artist_albums(artists['artists'][0]['id']))
    log.debug(netease.get_artist_albums(artists['artists'][0]['id']))

    assert netease._raw_request.call_count == 2


def test_18_get_album_info(netease):
    artists = netease.get_top_artists()
    albums = netease.get_artist_albums(artists['artists'][0]['id'])
    log.debug(netease.get_album_info(albums['hotAlbums'][0]['id']))
    log.debug(netease.get_album_info(albums['hotAlbums'][0]['id']))

    assert netease._raw_request.call_count == 3


def test_19_get_song_comments(netease):
    songs = netease.get_top_songs(0)
    log.debug(netease.get_song_comments(songs['playlist']['tracks'][0]['id']))
    log.debug(netease.get_song_comments(songs['playlist']['tracks'][0]['id']))

    assert netease._raw_request.call_count == 2


def test_20_get_songs_detail(netease):
    songs = netease.get_top_songs(0)
    log.debug(netease.get_songs_detail([songs['playlist']['tracks'][0]['id']]))
    log.debug(netease.get_songs_detail([songs['playlist']['tracks'][0]['id']]))

    assert netease._raw_request.call_count == 2


def test_21_get_songs_url(netease):
    songs = netease.get_top_songs(0)
    log.debug(netease.get_songs_url([songs['playlist']['tracks'][0]['id']], 0))
    log.debug(netease.get_songs_url([songs['playlist']['tracks'][0]['id']], 0))

    assert netease._raw_request.call_count == 2


def test_22_get_song_lyric(netease):
    songs = netease.get_top_songs(0)
    log.debug(netease.get_song_lyric(songs['playlist']['tracks'][0]['id']))
    log.debug(netease.get_song_lyric(songs['playlist']['tracks'][0]['id']))

    assert netease._raw_request.call_count == 2


def test_23_get_djchannels(netease):
    log.debug(netease.get_djchannels())
    log.debug(netease.get_djchannels())

    assert netease._raw_request.call_count == 1


def test_24_get_djprograms(netease):
    channels = netease.get_djchannels()
    log.debug(netease.get_djprograms(channels['djRadios'][0]['id']))
    log.debug(netease.get_djprograms(channels['djRadios'][0]['id']))

    assert netease._raw_request.call_count == 2


@pytest.mark.skip('需要登录')
def test_97_persistent_cache(netease, mocker):
    netease.get_user_playlist()
    assert os.path.exists(netease.request_cache.filepath)
    assert os.lstat(netease.request_cache.filepath).st_size > 0

    other = NetEaseApi(netease.config)
    mocker.patch.object(other, '_raw_request', side_effect=other._raw_request)
    other.get_user_playlist()

    assert other._raw_request.call_count == 0


@pytest.mark.skip('签到每天只能执行一次，不适合自动测试')
def test_98_daily_task(netease):
    netease.daily_task()
    netease.daily_task()

    assert netease._raw_request.call_count == 1
