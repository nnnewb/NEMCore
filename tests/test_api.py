import json

from nemcore import __version__
from nemcore.api import NetEaseApi


def test_version():
    assert __version__ == '0.1.5'


def test_00_login(api, username, password):
    api.login_if_need(username, password)


def test_02_login_refresh(api):
    api.login_refresh()


def test_03_get_user_playlist(api):
    resp = api.get_user_playlist()
    for playlist in resp.playlist:
        print(playlist.name)


def test_04_get_recommend_resource(api):
    resp = api.get_recommend_resource()
    for rec in resp.recommend:
        print(f'{rec.name} - {rec.playcount} 播放 - {rec.track_count} 首你可能喜欢的音乐')


def test_05_get_recommend_songs(api):
    resp = api.get_recommend_songs()
    for rec in resp.recommend:
        print(f'{rec.name} - {rec.album.name}')


def test_06_get_personal_fm(api):
    resp = api.get_personal_fm()
    print(json.dumps(resp))


def test_07_get_personal_fm_like(api):
    fm = api.get_personal_fm()
    resp = api.fm_like(fm['data'][0]['id'])


def test_08_get_personal_fm_trash(api):
    fm = api.get_personal_fm()
    resp = api.fm_trash(fm.data[0].id)


def test_09_search(api):
    resp = NetEaseApi().search('戦姫絶唱', offset=0, limit=20)
    for song in resp.result.songs:
        print(f'{song.name} - {song.artists[0].name}')


def test_10_get_new_albums(api):
    resp = api.get_new_albums()
    for album in resp.albums:
        print(album.name)


def test_11_get_top_playlists(api):
    resp = api.get_top_playlists()
    for pl in resp.playlists:
        print(pl.name)


def test_13_playlist_detail(api):
    resp = api.get_user_playlist()
    detail = api.get_playlist_detail(resp.playlist[0].id)
    for song in detail.playlist.tracks:
        print(f'{song.name} - {song.ar[0].name}')


def test_14_top_artists(api):
    resp = api.get_top_artists()
    for ar in resp.artists:
        print(ar.name)


def test_15_top_songs(api):
    resp = api.get_top_songs(0)
    for song in resp.playlist.tracks:
        print(song.name)


def test_16_get_artist_info(api):
    artists = api.get_top_artists()
    resp = api.get_artist_info(artists['artists'][0]['id'])
    print(resp.artist.name)


def test_17_get_artist_albums(api):
    artists = api.get_top_artists()
    resp = api.get_artist_albums(artists['artists'][0]['id'])
    for al in resp.hot_albums:
        print(al.name)


def test_18_get_album_info(api):
    artists = api.get_top_artists()
    albums = api.get_artist_albums(artists.artists[0].id)
    resp = api.get_album_info(albums.hot_albums[0].id)
    for song in resp.songs:
        print(song.name)


def test_19_get_song_comments(api):
    songs = api.get_top_songs(0)
    resp = api.get_song_comments(songs['playlist']['tracks'][0]['id'])
    for comment in resp.comments:
        print(comment.content)


def test_20_get_songs_detail(api):
    songs = api.get_top_songs(0)
    resp = api.get_songs_detail([songs['playlist']['tracks'][0]['id']])
    print(resp.songs[0].name)


def test_21_get_songs_url(api):
    songs = api.get_top_songs(0)
    resp = api.get_songs_url([songs['playlist']['tracks'][0]['id']], 0)
    print(resp.data[0].url)


def test_22_get_song_lyric(api):
    songs = api.get_top_songs(0)
    resp = api.get_song_lyric(songs['playlist']['tracks'][0]['id'])
    print(resp.lrc)


def test_23_get_dj_channels(api):
    resp = api.get_dj_channels()
    for radio in resp.dj_radios:
        print(radio.name)


def test_24_get_dj_programs(api):
    channels = api.get_dj_channels()
    resp = api.get_dj_programs(channels.dj_radios[0].id)
    for prog in resp.programs:
        print(prog.main_song.name)


def test_25_get_user_account(api):
    api.get_user_account()


def test_98_daily_task(api):
    api.daily_task()
