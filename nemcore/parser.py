class Parse(object):
    @classmethod
    def _song_url_by_id(cls, sid):
        # 128k
        url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(sid)
        quality = 'LD 128k'
        return url, quality

    @classmethod
    def song_url(cls, song):
        if 'url' in song:
            # get_songs_url resp
            url = song['url']
            if url is None:
                return Parse._song_url_by_id(song['id'])
            br = song['br']
            if br >= 320000:
                quality = 'HD'
            elif br >= 192000:
                quality = 'MD'
            else:
                quality = 'LD'
            return url, '{} {}k'.format(quality, br // 1000)
        else:
            # get_songs_detail resp
            return Parse._song_url_by_id(song['id'])

    @classmethod
    def song_album(cls, song):
        # 对新老接口进行处理
        if 'al' in song:
            if song['al'] is not None:
                album_name = song['al']['name']
                album_id = song['al']['id']
            else:
                album_name = '未知专辑'
                album_id = ''
        elif 'album' in song:
            if song['album'] is not None:
                album_name = song['album']['name']
                album_id = song['album']['id']
            else:
                album_name = '未知专辑'
                album_id = ''
        else:
            raise ValueError
        return album_name, album_id

    @classmethod
    def song_artist(cls, song):
        artist = ''
        # 对新老接口进行处理
        if 'ar' in song:
            artist = ', '.join(
                [a['name'] for a in song['ar'] if a['name'] is not None])
            # 某些云盘的音乐会出现 'ar' 的 'name' 为 None 的情况
            # 不过会多个 ’pc' 的字段
            # {'name': '简单爱', 'id': 31393663, 'pst': 0, 't': 1, 'ar': [{'id': 0, 'name': None, 'tns': [], 'alias': []}],
            #  'alia': [], 'pop': 0.0, 'st': 0, 'rt': None, 'fee': 0, 'v': 5, 'crbt': None, 'cf': None,
            #  'al': {'id': 0, 'name': None, 'picUrl': None, 'tns': [], 'pic': 0}, 'dt': 273000, 'h': None, 'm': None,
            #  'l': {'br': 193000, 'fid': 0, 'size': 6559659, 'vd': 0.0}, 'a': None, 'cd': None, 'no': 0, 'rtUrl': None,
            #  'ftype': 0, 'rtUrls': [], 'djId': 0, 'copyright': 0, 's_id': 0, 'rtype': 0, 'rurl': None, 'mst': 9,
            #  'cp': 0, 'mv': 0, 'publishTime': 0,
            #  'pc': {'nickname': '', 'br': 192, 'fn': '简单爱.mp3', 'cid': '', 'uid': 41533322, 'alb': 'The One 演唱会',
            #         'sn': '简单爱', 'version': 2, 'ar': '周杰伦'}, 'url': None, 'br': 0}
            if artist == '' and 'pc' in song:
                artist = '未知艺术家' if song['pc']['ar'] is None else song['pc'][
                    'ar']
        elif 'artists' in song:
            artist = ', '.join([a['name'] for a in song['artists']])
        else:
            artist = '未知艺术家'

        return artist

    @classmethod
    def songs(cls, songs):
        song_info_list = []
        for song in songs:
            url, quality = Parse.song_url(song)
            if not url:
                continue

            album_name, album_id = Parse.song_album(song)
            song_info = {
                'song_id': song['id'],
                'artist': Parse.song_artist(song),
                'song_name': song['name'],
                'album_name': album_name,
                'album_id': album_id,
                'mp3_url': url,
                'quality': quality,
                'expires': song['expires'],
                'get_time': song['get_time']
            }
            song_info_list.append(song_info)
        return song_info_list

    @classmethod
    def artists(cls, artists):
        return [{
            'artist_id': artist['id'],
            'artists_name': artist['name'],
            'alias': ''.join(artist['alias'])
        } for artist in artists]

    @classmethod
    def albums(cls, albums):
        return [{
            'album_id': album['id'],
            'albums_name': album['name'],
            'artists_name': album['artist']['name']
        } for album in albums]

    @classmethod
    def playlists(cls, playlists):
        return [{
            'playlist_id': pl['id'],
            'playlist_name': pl['name'],
            'creator_name': pl['creator']['nickname']
        } for pl in playlists]
