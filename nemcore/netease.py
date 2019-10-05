import json
import logging
import platform
import re
import time
from hashlib import md5
from http.cookiejar import Cookie, LWPCookieJar
from os.path import join as joinpath

import requests
from cachetools import cached, TTLCache

from nemcore import const as c
from nemcore.conf import Config
from nemcore.encrypt import encrypted_request
from nemcore.parser import Parse
from nemcore.storage import Storage
from nemcore.utils import raise_for_code

log = logging.getLogger(__name__)


class NetEase(object):
    def __init__(self, config=None):
        # yapf: disable
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',  # noqa: E501
        }
        # yapf: enable
        self.config = config or Config()
        storage_path = joinpath(self.config['DATA_DIR'], 'database.json')
        cookies_path = joinpath(self.config['DATA_DIR'], 'cookie')

        self.storage = Storage(storage_path)
        self.session = requests.Session()
        self.session.cookies = LWPCookieJar(cookies_path)

        try:
            self.session.cookies.load()
        except FileNotFoundError:
            self.session.cookies.save()

        for cookie in self.session.cookies:
            if cookie.is_expired():
                # QUESTION: 任何一个cookie过期都导致登出？
                self.session.cookies.clear()
                self.storage.logout()
                break

        self._set_base_cookies()

        self.ttl_cache = TTLCache(100, config['CACHE_TTL'])
        self.request = cached(self.ttl_cache)(self.request)

    def _set_base_cookies(self):
        """ 设置基础cookie

        无cookie时调用登录等接口会出现 -490 cheating 这样的错误

        reference:

        - [Issue #745](https://github.com/darknessomi/musicbox/issues/745)
        - [参考代码](https://github.com/Binaryify/NeteaseCloudMusicApi/commit/883d94580)
        """
        for name, value in c.BASE_COOKIES.items():
            cookie = self.make_cookie(name, value)
            self.session.cookies.set_cookie(cookie)

    def logout(self):
        """ 登出

        清除所有cookie和storage里的用户信息
        """
        self.storage.logout()
        self.session.cookies.clear()
        self._set_base_cookies()
        self.session.cookies.save()

    def _raw_request(self, method, endpoint, data=None):
        if method == 'GET':
            resp = self.session.get(endpoint,
                                    params=data,
                                    headers=self.header,
                                    timeout=c.DEFAULT_TIMEOUT)
        elif method == 'POST':
            resp = self.session.post(endpoint,
                                     data=data,
                                     headers=self.header,
                                     timeout=c.DEFAULT_TIMEOUT)
        return resp

    # 生成Cookie对象
    def make_cookie(self, name, value):
        return Cookie(version=0,
                      name=name,
                      value=value,
                      port=None,
                      port_specified=False,
                      domain="music.163.com",
                      domain_specified=True,
                      domain_initial_dot=False,
                      path="/",
                      path_specified=True,
                      secure=False,
                      expires=None,
                      discard=False,
                      comment=None,
                      comment_url=None,
                      rest={})

    def request(self,
                method,
                path,
                params=None,
                default=None,
                custom_cookies=None):
        if not params:
            params = {}

        if not default:
            default = {'code': -1}

        if not custom_cookies:
            custom_cookies = {}

        endpoint = '{}{}'.format(c.BASE_URL, path)
        csrf_token = ''
        for cookie in self.session.cookies:
            if cookie.name == '__csrf':
                csrf_token = cookie.value
                break
        params.update({'csrf_token': csrf_token})
        data = default

        for key, value in custom_cookies.items():
            cookie = self.make_cookie(key, value)
            self.session.cookies.set_cookie(cookie)

        params = encrypted_request(params)
        try:
            resp = self._raw_request(method, endpoint, params)
            data = resp.json()
        except ValueError as e:  # noqa: F841
            log.error('response:\n{}'.format(path, resp.text[:200]))
            raise

        raise_for_code(data)
        return data

    def login(self, username: str, password: str):
        """ 登录网易云音乐账号

        支持邮箱登录和手机号码登录，cookies 会自动持久化到 ~/.netease-musicbox/cookies
        返回登录结果。

        :param username: 用户名，如果是纯数字字符串，自动使用手机号码登录接口
        :param password: 密码
        :return: 正常返回字典 {...}，否则抛出异常
        """
        username = username.strip()
        password = md5(password.encode('utf-8')).hexdigest()
        self.session.cookies.load()

        if username.isdigit():
            path = '/weapi/login/cellphone'
            params = dict(
                phone=username,
                password=password,
                rememberLogin='true',
            )
        else:
            # magic token for login
            # see https://github.com/Binaryify/NeteaseCloudMusicApi/blob/master/router/login.js#L15
            client_token = '1_jVUMqWEPke0/1/Vu56xCmJpo5vP1grjn_SOVVDzOc78w8OKLVZ2JH7IfkjSXqgfmh'
            path = '/weapi/login'
            params = dict(
                username=username,
                password=password,
                rememberLogin='true',
                clientToken=client_token,
            )

        data = self.request('POST', path, params)
        self.session.cookies.save()

        if data['code'] == 200:
            self.storage.login(data['account'], data['profile'])

        return data

    def get_login_status(self) -> dict:
        """ 检查登录状态

        HACK: 根据云音乐首页的js里，某句GUser赋值的语句赋值内容是否是空对象，来判断是否登录。

        :return: 如果已经登录，返回用户信息字典，否则抛出异常
        """
        profile, bindings = None, None
        quote_regex = r'([\{\s,])(\w+)(:)'
        resp = self._raw_request('GET', c.BASE_URL)
        profile_result = re.search(r'GUser\s*=\s*([^;]+);', resp.text)
        bindings_result = re.search(r'GBinds\s*=\s*([^;]+);', resp.text)

        if not profile_result or not bindings_result:
            return {'code': 301, 'message': 'Not login'}

        if profile_result and profile_result.groups():
            text = profile_result.groups()[0]
            json_obj = re.sub(quote_regex, r'\1"\2"\3', text)
            profile = json.loads(json_obj)

        if bindings_result and bindings_result.groups():
            text = bindings_result.groups()[0]
            json_obj = re.sub(quote_regex, r'\1"\2"\3', text)
            bindings = json.loads(json_obj)

        if not profile or not bindings:
            return {'code': 301, 'message': 'Not login'}

        return {
            'code': 200,
            'message': 'ok',
            'profile': profile,
            'bindings': bindings
        }

    def login_refresh(self):
        """ 刷新登录状态

        :return: 成功返回{'code': 200}，反之抛出异常
        """
        data = self.request('GET', '/weapi/login/token/refresh')
        if data['code'] == -1:
            # 已知这个API会返回空的body，发现错误码是默认值-1时改成200
            data['code'] = 200
        return data

    def daily_task(self, is_mobile=True):
        """ 每日签到

        :param is_mobile: 是否是手机签到
        :return: 正常返回字典{point,code}，错误抛出异常
        """
        path = '/weapi/point/dailyTask'
        params = dict(type=0 if is_mobile else 1)
        return self.request('POST', path, params)

    def get_user_playlist(self, uid=None, offset=0, limit=50):
        """ 查看用户歌单

        :param uid: 用户ID,不传递时指自己的歌单
        :return: 正常返回 {code:int,more:bool,playlist:[]}
        """
        if not uid:
            uid = self.storage.uid
            if uid is None:
                raise ValueError('Not login .')
        path = '/weapi/user/playlist'
        params = dict(uid=uid, offset=offset, limit=limit, csrf_token='')
        return self.request('POST', path, params)

    def get_recommend_resource(self):
        """ 获得日推歌单列表。

        NOTE: 注意这个不是通常所说的日推，而是推荐的歌单列表，每日更新。

        NOTE: 日推请转到 `recommend_playlist`
        """
        path = '/weapi/v1/discovery/recommend/resource'
        return self.request('POST', path)

    def get_recommend_songs(self, total=True, offset=0, limit=20):
        """ 获得每日推荐歌曲
        """
        path = '/weapi/v1/discovery/recommend/songs'  # NOQA
        params = dict(total=total, offset=offset, limit=limit, csrf_token='')
        return self.request('POST', path, params)

    def get_personal_fm(self):
        """ 私人FM
        """
        path = '/weapi/v1/radio/get'
        return self.request('POST', path)

    def fm_like(self, songid, like=True, time=25, alg='itembased'):
        """ 私人FM操作：喜欢

        NOTE: 这个 API 可能影响云音乐今后的日推和FM结果。
        """
        path = '/weapi/radio/like'
        params = dict(alg=alg,
                      trackId=songid,
                      like='true' if like else 'false',
                      time=time)
        return self.request('POST', path, params)

    def fm_trash(self, songid, time=25, alg='RT'):
        """ 私人FM操作：不喜欢

        NOTE: 这个API可能影响云音乐今后的日推和FM结果。
        """
        path = '/weapi/radio/trash/add'
        params = dict(
            songId=songid,
            alg=alg,
            time=time,
        )
        return self.request('POST', path, params)

    def search(self, keywords, stype=1, offset=0, total='true', limit=50):
        """ 搜索歌曲

        :param keywords: 搜索关键词
        :param stype: 搜索类型，可选值：单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) *(type)*
        :param offset: 搜索结果偏移，和limit结合做分页
        :param total: TODO
        :param limit: 搜索结果集大小，和offset结合做分页
        """
        path = '/weapi/search/get'
        params = dict(s=keywords,
                      type=stype,
                      offset=offset,
                      total=total,
                      limit=limit)
        return self.request('POST', path, params)

    def get_new_albums(self, offset=0, limit=50):
        """ 新碟上架

        :param offset: 结果偏移，和limit结合做分页
        :param limit: 结果集大小，和offset结合做分页
        """
        path = '/weapi/album/new'
        params = dict(
            area='ALL',
            offset=offset,
            total=True,
            limit=limit,
        )
        return self.request('POST', path, params)

    def get_top_playlists(self, category='全部', order='hot', offset=0,
                          limit=50):
        """ 歌单（网友精选碟）

        对应[首页>>发现音乐>>歌单](http://music.163.com/#/discover/playlist/)

        :param category: 歌单分类
        :param order: 排序方法，可选值 TODO
        :param offset: 结果偏移，和Limit结合做分页
        :param limit: 结果集大小，和offset结合做分页
        """
        path = '/weapi/playlist/list'
        params = dict(cat=category,
                      order=order,
                      offset=offset,
                      total='true',
                      limit=limit)
        return self.request('POST', path, params)

    def playlist_catelogs(self):
        """ catalogs
        """
        path = '/weapi/playlist/catalogue'
        return self.request('POST', path)

    def get_playlist_detail(self, playlist_id):
        """ 歌单详情

        :param playlist_id: 歌单ID
        """
        path = '/weapi/v3/playlist/detail'
        params = dict(id=playlist_id,
                      total='true',
                      limit=1000,
                      n=1000,
                      offest=0)
        # cookie添加os字段
        custom_cookies = dict(os=platform.system())
        return self.request('POST', path, params, {'code': -1}, custom_cookies)

    def get_top_artists(self, offset=0, limit=100):
        """ 热门歌手

        对应[首页>>发现音乐>>歌手](https://music.163.com/#/discover/artist/)

        :param offset: 结果偏移，和Limit结合做分页
        :param limit: 结果集大小，和offset结合做分页
        """
        path = '/weapi/artist/top'
        params = dict(offset=offset, total=True, limit=limit)
        return self.request('POST', path, params)

    def get_top_songs(self, idx=0, offset=0, limit=100):
        """ 热门单曲榜

        对应[首页>>发现音乐>>排行榜](https://music.163.com/#/discover/toplist?id=3779629)

        :param idx: 榜单ID，参考 netease.TOP_LIST_ALL
        :param offset: 结果偏移，和Limit结合做分页
        :param limit: 结果集大小，和offset结合做分页
        """
        playlist_id = c.TOP_LIST_ALL[idx][1]
        return self.get_playlist_detail(playlist_id)

    def get_artist_info(self, artist_id):
        """ 获取歌手信息

        包括热门单曲等。

        :param artist_id: 歌手ID
        """
        path = '/weapi/v1/artist/{}'.format(artist_id)
        return self.request('POST', path)

    def get_artist_albums(self, artist_id, offset=0, limit=50):
        """ 获取歌手专辑

        :param artist_id: 歌手ID
        :param offset: 结果偏移，和Limit结合做分页
        :param limit: 结果集大小，和offset结合做分页
        """
        path = '/weapi/artist/albums/{}'.format(artist_id)
        params = dict(offset=offset, total=True, limit=limit)
        return self.request('POST', path, params)

    def get_album_info(self, album_id):
        """ 获取专辑信息

        :param album_id: 专辑ID
        """
        path = '/weapi/v1/album/{}'.format(album_id)
        return self.request('POST', path)

    def get_song_comments(self, music_id, offset=0, total='false', limit=100):
        """ 获取歌曲评论

        :param music_id: 歌曲ID
        :param offset: 结果偏移，和Limit结合做分页
        :param total: TODO
        :param limit: 结果集大小，和offset结合做分页
        """
        path = '/weapi/v1/resource/comments/R_SO_4_{}/'.format(music_id)
        params = dict(rid=music_id, offset=offset, total=total, limit=limit)
        return self.request('POST', path, params)

    def get_songs_detail(self, ids):
        """ 获取歌曲详情

        :param ids: 歌曲ID列表
        """
        path = '/weapi/v3/song/detail'
        params = dict(
            c=json.dumps([{
                'id': _id
            } for _id in ids]),
            ids=json.dumps(ids),
        )
        return self.request('POST', path, params)

    def get_songs_url(self, ids, quality):
        """ 获取歌曲播放url

        :param ids: 歌曲id列表
        :param quality: 音质档次，可选值0-2，分别对应 320kbps,192kbps,128kbps 三种质量
        """
        rate_map = {0: 320000, 1: 192000, 2: 128000}

        path = '/weapi/song/enhance/player/url'
        params = dict(ids=ids, br=rate_map[quality])
        return self.request('POST', path, params)

    def get_song_lyric(self, music_id):
        """ 获取歌词

        ApiEndpoint: http://music.163.com/api/song/lyric?os=osx&id= &lv=-1&kv=-1&tv=-1

        :param music_id: 歌曲ID
        """
        path = '/weapi/song/lyric'
        params = dict(os='osx', id=music_id, lv=-1, kv=-1, tv=-1)
        return self.request('POST', path, params)

    def get_djchannels(self, offset=0, limit=50):
        """ 热门主播电台

        今日最热（0）, 本周最热（10），历史最热（20），最新节目（30）

        对应[首页>>发现音乐>>主播电台](https://music.163.com/#/discover/djradio)
        """
        path = '/weapi/djradio/hot/v1'
        params = dict(limit=limit, offset=offset)
        return self.request('POST', path, params)

    def get_djprograms(self, radio_id, asc=False, offset=0, limit=50):
        """ 电台节目清单
        """
        path = '/weapi/dj/program/byradio'
        params = dict(asc=asc, radioId=radio_id, offset=offset, limit=limit)
        return self.request('POST', path, params)

    def dig_info(self, data, dig_type):
        if not data:
            return []

        if dig_type == 'songs' or dig_type == 'fmsongs':
            urls = self.get_songs_url([s['id'] for s in data])
            timestamp = time.time()
            # api 返回的 urls 的 id 顺序和 data 的 id 顺序不一致
            # 为了获取到对应 id 的 url，对返回的 urls 做一个 id2index 的缓存
            # 同时保证 data 的 id 顺序不变
            url_id_index = {}
            for index, url in enumerate(urls):
                url_id_index[url['id']] = index
            for s in data:
                url_index = url_id_index.get(s['id'])
                if url_index is None:
                    log.error("can't get song url, id: %s", s['id'])
                    continue
                s['url'] = urls[url_index]['url']
                s['br'] = urls[url_index]['br']
                s['expires'] = urls[url_index]['expi']
                s['get_time'] = timestamp
            return Parse.songs(data)
        elif dig_type == 'refresh_urls':
            urls_info = self.get_songs_url(data)
            timestamp = time.time()

            songs = []
            for url_info in urls_info:
                song = {}
                song['song_id'] = url_info['id']
                song['mp3_url'] = url_info['url']
                song['expires'] = url_info['expi']
                song['get_time'] = timestamp
                songs.append(song)
            return songs
        elif dig_type == 'artists':
            return Parse.artists(data)
        elif dig_type == 'albums':
            return Parse.albums(data)
        elif dig_type == 'playlists' or dig_type == 'top_playlists':
            return Parse.playlists(data)
        elif dig_type == 'playlist_classes':
            return list(c.PLAYLIST_CLASSES.keys())
        elif dig_type == 'playlist_class_detail':
            return c.PLAYLIST_CLASSES[data]
        else:
            raise ValueError('Invalid dig type')
