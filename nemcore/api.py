""" 网易云音乐的核心 HTTP API 客户端模块
"""
import json
import logging
import platform
import re
from hashlib import md5
from http.cookiejar import CookieJar, LWPCookieJar
from typing import Mapping, Sequence

import requests

from nemcore import const as c
from nemcore.encrypt import encrypted_request
from nemcore.utils import make_cookie, raise_for_code
from nemcore.utils.cache import cache_fn

log = logging.getLogger(__name__)


class NetEaseApi(object):
    def __init__(self,
                 cookie_path: str = None,
                 cache_path: str = None,
                 cache_ttl: int = 300):
        """ 网易云音乐 HTTP Api 客户端

        :param cookie_path: cookies 本地保存路径。如果不设置，则不会持久化cookies。
        :param cache_path: 网络请求的本地缓存路径，如果不设置，则只在内存缓存。
        :param cache_ttl: 请求缓存的保留时间。
        """
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
        self.session = requests.Session()
        jar = LWPCookieJar(cookie_path) if cookie_path else CookieJar()
        self.session.cookies = jar

        for cookie in self.session.cookies:
            if cookie.is_expired():
                # QUESTION: 任何一个cookie过期都导致登出？
                self.session.cookies.clear()
                break

        self._set_base_cookies()
        self.setup_cache(fpath=cache_path)

        # login status
        self.profile = None

    def _set_base_cookies(self):
        """ 设置基础cookie

        无cookie时调用登录等接口会出现 -490 cheating 这样的错误

        reference:

        - [Issue #745](https://github.com/darknessomi/musicbox/issues/745)
        - [参考代码](https://github.com/Binaryify/NeteaseCloudMusicApi/commit/883d94580)
        """
        for name, value in c.BASE_COOKIES.items():
            cookie = make_cookie(name, value)
            self.session.cookies.set_cookie(cookie)

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

    @property
    def uid(self):
        """ 用户的id

        未登录时为None
        """
        if self.profile:
            return self.profile['userId']
        return None

    def setup_cache(self, ttl=300, fpath=None):
        """ 配置指定请求的缓存参数

        允许指定缓存文件位置和缓存的保留时间。

        NOTE: 通过monkey patch实现，替换了 :meth:`request` 的实现。

        :param ttl: 缓存时间，单位秒
        :param fpath: 缓存文件位置，如果传入None则认为不持久化。
        :return:
        """
        # cache setup
        if fpath:
            self.request_cache, self.request = cache_fn(self.request,
                                                        ttl,
                                                        filepath=fpath)
        else:
            self.request_cache, self.request = cache_fn(self.request, ttl)

    def request(self,
                method: str,
                path: str,
                params: Mapping = None,
                default: Mapping = None,
                custom_cookies: Mapping = None) -> Mapping:
        """ 发送请求

        这个函数会准备好csrf token、将请求的api路径转换为合法的url、处理并保存cookies。

        如果服务器返回的响应提示错误，会抛出``NetEaseError``。

        :param method: 请求的HTTP方法
        :param path: 请求的API路径
        :param params: 请求的参数，当方法是GET时使用Query String传递，使用POST时使用form传递。
        :param default: 响应内容为空时或无效时使用的默认响应内容，注意``message``字段会在无法解析响应json时替换成``unable to decode response``。
        :param custom_cookies: 自定义的cookies，注意，这些cookies会在本次会话中一直存在，直到你退出登录或被服务器丢弃。
        :return: 返回服务端的响应内容
        """
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
            cookie = make_cookie(key, value)
            self.session.cookies.set_cookie(cookie)

        params = encrypted_request(params)
        try:
            resp = self._raw_request(method, endpoint, params)
            data = resp.json()
        except (json.JSONDecodeError, ValueError) as e:  # noqa: F841
            log.error('response:\n{}'.format(path, resp.text[:200]))
            data['message'] = 'unable to decode response'
            return data

        raise_for_code(data)
        return data

    def clear_cache(self):
        """ 清除请求缓存
        """
        self.request_cache.clear()

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
        if data.get('code', -1) == 200:
            self.profile = data['profile']

        if isinstance(self.session.cookies, LWPCookieJar):
            self.session.cookies.save()

        return data

    def logout(self):
        """ 登出

        清除所有cookie和storage里的用户信息
        """
        self.profile = None
        self.session.cookies.clear()
        self._set_base_cookies()
        self.session.cookies.save()

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

        :return: 不返回
        """
        method = 'GET'
        url = c.BASE_URL + '/weapi/login/token/refresh'
        resp = self._raw_request(method, url, {})
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            raise_for_code({'code': -1, 'message': str(e)}, method, url)

    def daily_task(self, is_mobile: bool = True):
        """ 每日签到

        :param is_mobile: 是否是手机签到
        :return: 正常返回字典{point,code}，错误抛出异常
        """
        path = '/weapi/point/dailyTask'
        params = dict(type=0 if is_mobile else 1)
        return self.request('POST', path, params)

    def get_user_playlist(self,
                          uid: int = None,
                          offset: int = 0,
                          limit: int = 50):
        """ 查看用户歌单

        :param uid: 用户ID,不传递时指自己的歌单
        :return: 正常返回 {code:int,more:bool,playlist:[]}
        """
        if not uid and not self.uid:
            raise ValueError('尚未登陆。')

        path = '/weapi/user/playlist'
        params = dict(uid=uid or self.uid,
                      offset=offset,
                      limit=limit,
                      csrf_token='')
        return self.request('POST', path, params)

    def get_recommend_resource(self):
        """ 获得日推歌单列表。

        NOTE: 注意这个不是通常所说的日推，而是推荐的歌单列表，每日更新。

        NOTE: 日推请转到 `recommend_playlist`
        """
        path = '/weapi/v1/discovery/recommend/resource'
        return self.request('POST', path)

    def get_recommend_songs(self,
                            total: bool = True,
                            offset: int = 0,
                            limit: int = 20):
        """ 获得每日推荐歌曲
        """
        path = '/weapi/v1/discovery/recommend/songs'  # NOQA
        params = dict(total='true' if total else 'false',
                      offset=offset,
                      limit=limit,
                      csrf_token='')
        return self.request('POST', path, params)

    def get_personal_fm(self):
        """ 私人FM
        """
        path = '/weapi/v1/radio/get'
        return self.request('POST', path)

    def fm_like(self,
                songid: int,
                like: bool = True,
                time: int = 25,
                alg: str = 'itembased'):
        """ 私人FM操作：喜欢

        NOTE: 这个 API 可能影响云音乐今后的日推和FM结果。
        """
        path = '/weapi/radio/like'
        params = dict(alg=alg,
                      trackId=songid,
                      like='true' if like else 'false',
                      time=time)
        return self.request('POST', path, params)

    def fm_trash(self, songid: int, time: int = 25, alg: str = 'RT'):
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

    def search(self,
               keywords: str,
               stype: int = 1,
               total: bool = True,
               offset: int = 0,
               limit: int = 50):
        """ 搜索歌曲

        :param keywords: 搜索关键词
        :param stype: 搜索类型，可选值：单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) *(type)*
        :param total: TODO
        :param offset: 搜索结果偏移，和limit结合做分页
        :param limit: 搜索结果集大小，和ofset结合做分页
        """
        path = '/weapi/search/get'
        params = dict(s=keywords,
                      type=stype,
                      offset=offset,
                      total=total,
                      limit=limit)
        return self.request('POST', path, params)

    def get_new_albums(self, offset: int = 0, limit: int = 50):
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

    def get_top_playlists(self,
                          category: str = '全部',
                          order: str = 'hot',
                          offset: int = 0,
                          limit: int = 50):
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

    def get_playlist_detail(self, playlist_id: int):
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

    def get_top_artists(self, offset: int = 0, limit: int = 100):
        """ 热门歌手

        对应[首页>>发现音乐>>歌手](https://music.163.com/#/discover/artist/)

        :param offset: 结果偏移，和Limit结合做分页
        :param limit: 结果集大小，和offset结合做分页
        """
        path = '/weapi/artist/top'
        params = dict(offset=offset, total=True, limit=limit)
        return self.request('POST', path, params)

    def get_top_songs(self, idx: int = 0, offset: int = 0, limit: int = 100):
        """ 热门单曲榜

        对应[首页>>发现音乐>>排行榜](https://music.163.com/#/discover/toplist?id=3779629)

        :param idx: 榜单ID，参考 netease.TOP_LIST_ALL
        :param offset: 结果偏移，和Limit结合做分页
        :param limit: 结果集大小，和offset结合做分页
        """
        playlist_id = c.TOP_LIST_ALL[idx][1]
        return self.get_playlist_detail(playlist_id)

    def get_artist_info(self, artist_id: int):
        """ 获取歌手信息

        包括热门单曲等。

        :param artist_id: 歌手ID
        """
        path = '/weapi/v1/artist/{}'.format(artist_id)
        return self.request('POST', path)

    def get_artist_albums(self,
                          artist_id: int,
                          offset: int = 0,
                          limit: int = 50):
        """ 获取歌手专辑

        :param artist_id: 歌手ID
        :param offset: 结果偏移，和Limit结合做分页
        :param limit: 结果集大小，和offset结合做分页
        """
        path = '/weapi/artist/albums/{}'.format(artist_id)
        params = dict(offset=offset, total=True, limit=limit)
        return self.request('POST', path, params)

    def get_album_info(self, album_id: int):
        """ 获取专辑信息

        :param album_id: 专辑ID
        """
        path = '/weapi/v1/album/{}'.format(album_id)
        return self.request('POST', path)

    def get_song_comments(self,
                          music_id: int,
                          total: bool = False,
                          offset: int = 0,
                          limit: int = 100):
        """ 获取歌曲评论

        :param music_id: 歌曲ID
        :param offset: 结果偏移，和Limit结合做分页
        :param total: TODO
        :param limit: 结果集大小，和offset结合做分页
        """
        path = '/weapi/v1/resource/comments/R_SO_4_{}/'.format(music_id)
        params = dict(rid=music_id,
                      offset=offset,
                      total='true' if total else 'false',
                      limit=limit)
        return self.request('POST', path, params)

    def get_songs_detail(self, ids: Sequence[int]):
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

    def get_songs_url(self, ids: Sequence[int], quality: int):
        """ 获取歌曲播放url

        :param ids: 歌曲id列表
        :param quality: 音质档次，可选值0-2，分别对应 320kbps,192kbps,128kbps 三种质量
        """
        rate_map = {0: 320000, 1: 192000, 2: 128000}

        path = '/weapi/song/enhance/player/url'
        params = dict(ids=ids, br=rate_map[quality])
        return self.request('POST', path, params)

    def get_song_lyric(self, music_id: int):
        """ 获取歌词

        ApiEndpoint: http://music.163.com/api/song/lyric?os=osx&id= &lv=-1&kv=-1&tv=-1

        :param music_id: 歌曲ID
        """
        path = '/weapi/song/lyric'
        params = dict(os='osx', id=music_id, lv=-1, kv=-1, tv=-1)
        return self.request('POST', path, params)

    def get_djchannels(self, offset: int = 0, limit: int = 50):
        """ 热门主播电台

        今日最热（0）, 本周最热（10），历史最热（20），最新节目（30）

        对应[首页>>发现音乐>>主播电台](https://music.163.com/#/discover/djradio)
        """
        path = '/weapi/djradio/hot/v1'
        params = dict(limit=limit, offset=offset)
        return self.request('POST', path, params)

    def get_djprograms(self,
                       radio_id: int,
                       asc: bool = False,
                       offset: int = 0,
                       limit: int = 50):
        """ 电台节目清单
        """
        path = '/weapi/dj/program/byradio'
        params = dict(asc=asc, radioId=radio_id, offset=offset, limit=limit)
        return self.request('POST', path, params)
