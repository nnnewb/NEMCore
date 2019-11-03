快速开始
=========

`nemcore`_ 是从 `netease-musicbox`_ 项目抽取的核心api模块，简化重构后的产物。

.. _nemcore: https://github.com/nnnewb/NEMCore
.. _netease-musicbox: https://github.com/darknessomi/musicbox/

使用nemcore可以实现一个简单的网易云音乐播放器。

安装
-----

你可以使用pip安装。::

    pip install nemcore

登录
--------

使用 :meth:`nemcore.api.NetEaseApi.login` 接口登录。

登录信息会保存在cookie中，如需保存登录状态，可以在初始化 :class:`nemcore.api.NetEaseApi`
实例时传入 ``cookie_path`` 参数。

下次初始化 :class:`nemcore.api.NetEaseApi` 实例时会自动加载登录状态。

例子::

    from nemcore.api import NetEaseApi

    box = NetEaseApi(cookie_path='./cookies')
    box.login('cloudmusic@163.com', 'password')
    print(box.uid)

上面的例子代码应该输出你的用户id。

如果登陆失败，上面的代码会抛出 :class:`nemcore.exceptions.NetEaseError` ，异常对象的
``code`` 和 ``message`` 属性描述了错误的原因。

你还可以从``box.profile``属性获得当前用户的更多信息。::

    print(box.profile)

美化后的输出类似于下面的样子（部分数据隐藏）：::

    {
        'userId': *********,
        'vipType': **,
        'gender': 0,
        'accountStatus': 0,
        'avatarImgId': 109951164454534888,
        'nickname': 'RunePiika',
        'birthday': **************,
        'city': ******,
        'backgroundImgId': 2002210674180201,
        'expertTags': None,
        'authStatus': 0,
        'backgroundUrl': 'http://p1.music.126.net/o3G7lWrGBQAvSRt3UuApTw==/2002210674180201.jpg',
        'detailDescription': '',
        'followed': False,
        'description': '',
        'avatarImgIdStr': '109951164454534888',
        'backgroundImgIdStr': '2002210674180201',
        'signature': '',
        'authority': 0,
        'avatarImgId_str': '109951164454534888',
        'followeds': 0,
        'follows': 2,
        'eventCount': 0,
        'playlistCount': 6,
        'playlistBeSubscribedCount': 0
    }

登出
-------

如果需要登出，可以调用 :meth:`nemcore.api.NetEaseApi.logout`。::

    from nemcore.api import NetEaseApi

    box = NetEaseApi(cookie_path='./cookies')
    box.login('cloudmusic@163.com', 'password')
    box.logout()

登出后，磁盘上持久化的登录cookie会立即清除。


收藏的歌单
------------

通过 :meth:`nemcore.api.NetEaseApi.get_user_playlist` 来获取用户的歌单清单::

    from nemcore.api import NetEaseApi

    box = NetEaseApi(cookie_path='./cookies')
    box.login('cloudmusic@163.com', 'password')

    result = box.get_user_playlist()
    print(result)

输出结果如下（截取）::

    {
        'code': 200,
        'more': False,
        'playlist': [
            ......,
            {
                "subscribers": [],
                "subscribed": false,
                "creator": {
                    "defaultAvatar": false,
                    "province": 440000,
                    "authStatus": 0,
                    "followed": false,
                    "avatarUrl": "http://p1.music.126.net/HYH88XVn0K5U_v-dofshiA==/109951164454534888.jpg",
                    "accountStatus": 0,
                    "gender": 0,
                    "city": 440100,
                    "birthday": -2209017600000,
                    "userId": 123860360,
                    "userType": 0,
                    "nickname": "RunePiika",
                    "signature": "",
                    "description": "",
                    "detailDescription": "",
                    "avatarImgId": 109951164454534888,
                    "backgroundImgId": 2002210674180201,
                    "backgroundUrl": "http://p1.music.126.net/o3G7lWrGBQAvSRt3UuApTw==/2002210674180201.jpg",
                    "authority": 0,
                    "mutual": false,
                    "expertTags": null,
                    "experts": null,
                    "djStatus": 0,
                    "vipType": 11,
                    "remarkName": null,
                    "avatarImgIdStr": "109951164454534888",
                    "backgroundImgIdStr": "2002210674180201",
                    "avatarImgId_str": "109951164454534888"
                },
                "artists": null,
                "tracks": null,
                "updateFrequency": null,
                "backgroundCoverId": 0,
                "backgroundCoverUrl": null,
                "titleImage": 0,
                "titleImageUrl": null,
                "englishTitle": null,
                "opRecommend": false,
                "ordered": false,
                "tags": [],
                "createTime": 1570005044850,
                "highQuality": false,
                "userId": 123860360,
                "trackUpdateTime": 1570440713851,
                "trackCount": 96,
                "coverImgId": 109951164200702033,
                "newImported": false,
                "anonimous": false,
                "updateTime": 1570259034591,
                "playCount": 19,
                "trackNumberUpdateTime": 1570259034591,
                "specialType": 0,
                "commentThreadId": "A_PL_0_3010890240",
                "privacy": 0,
                "coverImgUrl": "http://p1.music.126.net/z8vqN5OzDwrHoEjlslchmQ==/109951164200702033.jpg",
                "totalDuration": 0,
                "adType": 0,
                "description": "",
                "status": 0,
                "subscribedCount": 0,
                "cloudTrackCount": 0,
                "name": "戦姫絶唱 Complete",
                "id": 3010890240,
                "coverImgId_str": "109951164200702033"
            },
            ......
        ]
    }

对于有非常多歌单的，可以用 ``offset`` 和 ``limit`` 参数分页获取。这里不做更多说明了。

歌单详情
-------------

通过 :meth:`nemcore.api.NetEaseApi.get_playlist_detail` 获取歌单的详情。::

    from nemcore.api import NetEaseApi

    box = NetEaseApi(cookie_path='./cookies')
    box.login('cloudmusic@163.com', 'password')

    result = box.get_user_playlist()
    playlist = result['playlist'][2]
    resp = box.get_playlist_detail(playlist['id'])
    print(resp)

获取的歌单详情输出如下：::

    {
        "code": 200,
        "relatedVideos": null,
        "playlist": {
            "subscribers": [],
            "subscribed": false,
            "creator": {
                "defaultAvatar": false,
                "province": 440000,
                "authStatus": 0,
                "followed": false,
                "avatarUrl": "http://p1.music.126.net/HYH88XVn0K5U_v-dofshiA==/109951164454534888.jpg",
                "accountStatus": 0,
                "gender": 0,
                "city": 440100,
                "birthday": -2209017600000,
                "userId": 123860360,
                "userType": 0,
                "nickname": "RunePiika",
                "signature": "",
                "description": "",
                "detailDescription": "",
                "avatarImgId": 109951164454534888,
                "backgroundImgId": 2002210674180201,
                "backgroundUrl": "http://p1.music.126.net/o3G7lWrGBQAvSRt3UuApTw==/2002210674180201.jpg",
                "authority": 0,
                "mutual": false,
                "expertTags": null,
                "experts": null,
                "djStatus": 0,
                "vipType": 11,
                "remarkName": null,
                "avatarImgIdStr": "109951164454534888",
                "backgroundImgIdStr": "2002210674180201",
                "avatarImgId_str": "109951164454534888"
            },
            "tracks": [
                {
                    "name": "Lasting Song",
                    "id": 1376680574,
                    "pst": 0,
                    "t": 0,
                    "ar": [
                        {
                            "id": 17955,
                            "name": "高垣彩陽",
                            "tns": [],
                            "alias": []
                        }
                    ],
                    "alia": [
                        "TV动画《战姬绝唱SYMPHOGEAR XV》片尾曲"
                    ],
                    "pop": 70.0,
                    "st": 0,
                    "rt": "",
                    "fee": 8,
                    "v": 4,
                    "crbt": null,
                    "cf": "",
                    "al": {
                        "id": 80276605,
                        "name": "Lasting Song",
                        "picUrl": "http://p2.music.126.net/z8vqN5OzDwrHoEjlslchmQ==/109951164200702033.jpg",
                        "tns": [],
                        "pic_str": "109951164200702033",
                        "pic": 109951164200702033
                    },
                    "dt": 269722,
                    "h": {
                        "br": 320000,
                        "fid": 0,
                        "size": 10789660,
                        "vd": -76637.0
                    },
                    "m": {
                        "br": 192000,
                        "fid": 0,
                        "size": 6473813,
                        "vd": -74134.0
                    },
                    "l": {
                        "br": 128000,
                        "fid": 0,
                        "size": 4315890,
                        "vd": -72739.0
                    },
                    "a": null,
                    "cd": "01",
                    "no": 1,
                    "rtUrl": null,
                    "ftype": 0,
                    "rtUrls": [],
                    "djId": 0,
                    "copyright": 0,
                    "s_id": 0,
                    "mark": 8192,
                    "mv": 0,
                    "rtype": 0,
                    "rurl": null,
                    "mst": 9,
                    "cp": 754011,
                    "publishTime": 0
                },
                ......
            ],
            "trackIds": [
                {
                    "id": 1376680574,
                    "v": 5,
                    "alg": null
                },
                {
                    "id": 1305366683,
                    "v": 5,
                    "alg": null
                },
                {
                    "id": 534067239,
                    "v": 6,
                    "alg": null
                },
                ......
            ],
            "updateFrequency": null,
            "backgroundCoverId": 0,
            "backgroundCoverUrl": null,
            "titleImage": 0,
            "titleImageUrl": null,
            "englishTitle": null,
            "opRecommend": false,
            "ordered": false,
            "status": 0,
            "adType": 0,
            "trackNumberUpdateTime": 1570259034591,
            "createTime": 1570005044850,
            "highQuality": false,
            "userId": 123860360,
            "updateTime": 1570259034591,
            "coverImgId": 109951164200702033,
            "newImported": false,
            "specialType": 0,
            "coverImgUrl": "http://p2.music.126.net/z8vqN5OzDwrHoEjlslchmQ==/109951164200702033.jpg",
            "commentThreadId": "A_PL_0_3010890240",
            "trackCount": 96,
            "privacy": 0,
            "trackUpdateTime": 1570440713851,
            "playCount": 19,
            "description": "",
            "tags": [],
            "subscribedCount": 0,
            "cloudTrackCount": 0,
            "name": "戦姫絶唱 Complete",
            "id": 3010890240,
            "shareCount": 0,
            "coverImgId_str": "109951164200702033",
            "commentCount": 0
        },
        "urls": null,
        "privileges": [
            {
                "id": 1376680574,
                "fee": 8,
                "payed": 1,
                "st": 0,
                "pl": 320000,
                "dl": 320000,
                "sp": 7,
                "cp": 1,
                "subp": 1,
                "cs": false,
                "maxbr": 320000,
                "fl": 128000,
                "toast": false,
                "flag": 132,
                "preSell": false
            },
            ......
        ]
    }


日推歌单
--------


通过 :meth:`nemcore.api.NetEaseApi.get_recommend_songs` 获取你的今日推荐。

需要登录才能调用，否则会出现错误代码 ``301``。

参考下面的例子调用：::

    from nemcore.api import NetEaseApi

    box = NetEaseApi()
    result = box.get_recommend_songs()
    print(result)

最终输出非常长，截取一部分如下：::

    {
        'code': 200,
        'recommend': [
            {
                'name': '雪よ舞い散れ其方に向けて',
                'id': 466794934,
                'position': 0,
                'alias': [],
                'status': 0,
                'fee': 8,
                'copyrightId': 457010,
                'disc': '1',
                'no': 5,
                'artists': [
                    {
                        'name': '和楽器バンド',
                        'id': 906077,
                        'picId': 0,
                        'img1v1Id': 0,
                        'briefDesc': '',
                        'picUrl': 'http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg',
                        'img1v1Url': 'http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg',
                        'albumSize': 0,
                        'alias': [],
                        'trans': '',
                        'musicSize': 0,
                        'topicPerson': 0
                    }
                ],
                'album': {
                    'name': '四季彩-shikisai-',
                    'id': 35292444,
                    'type': '专辑',
                    'size': 16,
                    'picId': 18535567022899061,
                    'blurPicUrl': 'http://p2.music.126.net/8pIIIOpj9yvG1q1KrLnpxg==/18535567022899061.jpg',
                    'companyId': 0,
                    'pic': 18535567022899061,
                    'picUrl': 'http://p2.music.126.net/8pIIIOpj9yvG1q1KrLnpxg==/18535567022899061.jpg',
                    'publishTime': 1490112000007,
                    'description': '',
                    'tags': '',
                    'company': '(P)2017 AVEX ENTERTAINMENT INC.',
                    'briefDesc': '',
                    'artist': {
                        'name': '',
                        'id': 0,
                        'picId': 0,
                        'img1v1Id': 0,
                        'briefDesc': '',
                        'picUrl': 'http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg',
                        'img1v1Url': 'http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg',
                        'albumSize': 0,
                        'alias': [],
                        'trans': '',
                        'musicSize': 0,
                        'topicPerson': 0
                    },
                    'songs': [],
                    'alias': [],
                    'status': 1,
                    'copyrightId': 457010,
                    'commentThreadId': 'R_AL_3_35292444',
                    'artists': [
                        {
                            'name': '和楽器バンド',
                            'id': 906077,
                            'picId': 0,
                            'img1v1Id': 0,
                            'briefDesc': '',
                            'picUrl': 'http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg',
                            'img1v1Url': 'http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg',
                            'albumSize': 0,
                            'alias': [],
                            'trans': '',
                            'musicSize': 0,
                            'topicPerson': 0
                        }
                    ],
                    'subType': '录音室版',
                    'transName': None,
                    'mark': 0,
                    'picId_str': '18535567022899061'
                },
                'starred': False,
                'popularity': 100.0,
                'score': 100,
                'starredNum': 0,
                'duration': 252653,
                'playedNum': 0,
                'dayPlays': 0,
                'hearTime': 0,
                'ringtone': None,
                'crbt': None,
                'audition': None,
                'copyFrom': '',
                'commentThreadId': 'R_SO_4_466794934',
                'rtUrl': None,
                'ftype': 0,
                'rtUrls': [],
                'copyright': 2,
                'transName': '雪落翩翩为君舞',
                'sign': None,
                'mark': 0,
                'mvid': 5773027,
                'bMusic': {
                    'name': None,
                    'id': 1293581984,
                    'size': 4043381,
                    'extension': 'mp3',
                    'sr': 44100,
                    'dfsId': 0,
                    'bitrate': 128000,
                    'playTime': 252653,
                    'volumeDelta': -32400.0
                },
                'mp3Url': None,
                'rtype': 0,
                'rurl': None,
                'hMusic': {
                    'name': None,
                    'id': 1293581982,
                    'size': 10108387,
                    'extension': 'mp3',
                    'sr': 44100,
                    'dfsId': 0,
                    'bitrate': 320000,
                    'playTime': 252653,
                    'volumeDelta': -36600.0
                },
                'mMusic': {
                    'name': None,
                    'id': 1293581983,
                    'size': 6065049,
                    'extension': 'mp3',
                    'sr': 44100,
                    'dfsId': 0,
                    'bitrate': 192000,
                    'playTime': 252653,
                    'volumeDelta': -34200.0
                },
                'lMusic': {
                    'name': None,
                    'id': 1293581984,
                    'size': 4043381,
                    'extension': 'mp3',
                    'sr': 44100,
                    'dfsId': 0,
                    'bitrate': 128000,
                    'playTime': 252653,
                    'volumeDelta': -32400.0
                },
                'transNames': ['雪落翩翩为君舞'],
                'privilege': {
                    'id': 466794934,
                    'fee': 8,
                    'payed': 1,
                    'st': 0,
                    'pl': 999000,
                    'dl': 999000,
                    'sp': 7,
                    'cp': 1,
                    'subp': 1,
                    'cs': False,
                    'maxbr': 999000,
                    'fl': 128000,
                    'toast': False,
                    'flag': 69,
                    'preSell': False
                },
                'reason': '根据你可能喜欢的单曲 Open your eyes',
                'alg': 'itembased'
            },
            ......
        ],
        'data': {
            'dailySongs': [
                {
                    "name": "雪よ舞い散れ其方に向けて",
                    "id": 466794934,
                    "position": 0,
                    "alias": [],
                    "status": 0,
                    "fee": 8,
                    "copyrightId": 457010,
                    "disc": "1",
                    "no": 5,
                    "artists": [
                        {
                            "name": "和楽器バンド",
                            "id": 906077,
                            "picId": 0,
                            "img1v1Id": 0,
                            "briefDesc": "",
                            "picUrl": "http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg",
                            "img1v1Url": "http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg",
                            "albumSize": 0,
                            "alias": [],
                            "trans": "",
                            "musicSize": 0,
                            "topicPerson": 0
                        }
                    ],
                    "album": {
                        "name": "四季彩-shikisai-",
                        "id": 35292444,
                        "type": "专辑",
                        "size": 16,
                        "picId": 18535567022899061,
                        "blurPicUrl": "http://p2.music.126.net/8pIIIOpj9yvG1q1KrLnpxg==/18535567022899061.jpg",
                        "companyId": 0,
                        "pic": 18535567022899061,
                        "picUrl": "http://p2.music.126.net/8pIIIOpj9yvG1q1KrLnpxg==/18535567022899061.jpg",
                        "publishTime": 1490112000007,
                        "description": "",
                        "tags": "",
                        "company": "(P)2017 AVEX ENTERTAINMENT INC.",
                        "briefDesc": "",
                        "artist": {
                            "name": "",
                            "id": 0,
                            "picId": 0,
                            "img1v1Id": 0,
                            "briefDesc": "",
                            "picUrl": "http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg",
                            "img1v1Url": "http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg",
                            "albumSize": 0,
                            "alias": [],
                            "trans": "",
                            "musicSize": 0,
                            "topicPerson": 0
                        },
                        "songs": [],
                        "alias": [],
                        "status": 1,
                        "copyrightId": 457010,
                        "commentThreadId": "R_AL_3_35292444",
                        "artists": [
                            {
                                "name": "和楽器バンド",
                                "id": 906077,
                                "picId": 0,
                                "img1v1Id": 0,
                                "briefDesc": "",
                                "picUrl": "http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg",
                                "img1v1Url": "http://p2.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg",
                                "albumSize": 0,
                                "alias": [],
                                "trans": "",
                                "musicSize": 0,
                                "topicPerson": 0
                            }
                        ],
                        "subType": "录音室版",
                        "transName": null,
                        "mark": 0,
                        "picId_str": "18535567022899061"
                    },
                    "starred": false,
                    "popularity": 100.0,
                    "score": 100,
                    "starredNum": 0,
                    "duration": 252653,
                    "playedNum": 0,
                    "dayPlays": 0,
                    "hearTime": 0,
                    "ringtone": null,
                    "crbt": null,
                    "audition": null,
                    "copyFrom": "",
                    "commentThreadId": "R_SO_4_466794934",
                    "rtUrl": null,
                    "ftype": 0,
                    "rtUrls": [],
                    "copyright": 2,
                    "transName": "雪落翩翩为君舞",
                    "sign": null,
                    "mark": 0,
                    "mvid": 5773027,
                    "bMusic": {
                        "name": null,
                        "id": 1293581984,
                        "size": 4043381,
                        "extension": "mp3",
                        "sr": 44100,
                        "dfsId": 0,
                        "bitrate": 128000,
                        "playTime": 252653,
                        "volumeDelta": -32400.0
                    },
                    "mp3Url": null,
                    "rtype": 0,
                    "rurl": null,
                    "hMusic": {
                        "name": null,
                        "id": 1293581982,
                        "size": 10108387,
                        "extension": "mp3",
                        "sr": 44100,
                        "dfsId": 0,
                        "bitrate": 320000,
                        "playTime": 252653,
                        "volumeDelta": -36600.0
                    },
                    "mMusic": {
                        "name": null,
                        "id": 1293581983,
                        "size": 6065049,
                        "extension": "mp3",
                        "sr": 44100,
                        "dfsId": 0,
                        "bitrate": 192000,
                        "playTime": 252653,
                        "volumeDelta": -34200.0
                    },
                    "lMusic": {
                        "name": null,
                        "id": 1293581984,
                        "size": 4043381,
                        "extension": "mp3",
                        "sr": 44100,
                        "dfsId": 0,
                        "bitrate": 128000,
                        "playTime": 252653,
                        "volumeDelta": -32400.0
                    },
                    "transNames": [
                        "雪落翩翩为君舞"
                    ],
                    "privilege": {
                        "id": 466794934,
                        "fee": 8,
                        "payed": 1,
                        "st": 0,
                        "pl": 999000,
                        "dl": 999000,
                        "sp": 7,
                        "cp": 1,
                        "subp": 1,
                        "cs": false,
                        "maxbr": 999000,
                        "fl": 128000,
                        "toast": false,
                        "flag": 69,
                        "preSell": false
                    },
                    "reason": "根据你可能喜欢的单曲 Open your eyes",
                    "alg": "itembased"
                },
                ......
            ],
            'orderSongs': [],
        }

搜索
--------

通过使用 :meth:`nemcore.api.NetEaseApi.search` 方法搜索歌曲，这个方法会返回一个歌曲清单。

    from nemcore.api import NetEaseApi
    from pprint import pprint

    box = NetEaseApi()
    pprint(box.search('戦姫絶唱'))

你可以看到如下输出。::

    {'code': 200,
     'result': {'songCount': 255,
                'songs': [{'album': {'artist': {'albumSize': 0,
                                            'alias': [],
                                            'id': 0,
                                            'img1v1': 0,
                                            'img1v1Url': 'http://p1.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg',
                                            'name': '',
                                            'picId': 0,
                                            'picUrl': None,
                                            'trans': None},
                                 'copyrightId': 756010,
                                 'id': 81107159,
                                 'mark': 0,
                                 'name': 'FINAL COMMANDER',
                                 'picId': 109951164316318410,
                                 'publishTime': 1566662400000,
                                 'size': 0,
                                 'status': 0},
                       'alias': ['TV动画《战姬绝唱SYMPHOGEAR XV》第一话插曲'],
                       'artists': [{'albumSize': 0,
                                    'alias': [],
                                    'id': 17028,
                                    'img1v1': 0,
                                    'img1v1Url': 'http://p1.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg',
                                    'name': '水樹奈々',
                                    'picId': 0,
                                    'picUrl': None,
                                    'trans': None}],
                       'copyrightId': 756010,
                       'duration': 262403,
                       'fee': 8,
                       'ftype': 0,
                       'id': 1386091650,
                       'mark': 8192,
                       'mvid': 0,
                       'name': 'FINAL COMMANDER',
                       'rUrl': None,
                       'rtype': 0,
                       'status': 0},
                       ......

下载mp3
------------

通过 :meth:`nemcore.api.NetEaseApi.get_songs_url` 来获取歌曲播放链接。::

    from nemcore.api import NetEaseApi

    box = NetEaseApi()
    # 取搜索结果的第一首歌
    song = box.search('戦姫絶唱')['result']['songs'][0]
    # 获取这首歌的详情
    resp = box.get_songs_url([song['id']])
    print(resp)

输出结果美化后如下。::

    {
        'data': [
            {
                'id': 1386091650,
                'url': 'http://m10.music.126.net/20191102213111/c61cb1830a15f9513a42df782433d073/ymusic/550f/0e59/015d/be32fcea1893e032f2ef675babf492eb.mp3',
                'br': 128000,
                'size': 4199697,
                'md5': 'be32fcea1893e032f2ef675babf492eb',
                'code': 200,
                'expi': 1200,
                'type': 'mp3',
                'gain': 0.0,
                'fee': 8,
                'uf': None,
                'payed': 0,
                'flag': 68,
                'canExtend': False,
                'freeTrialInfo': None,
                'level': 'standard',
                'encodeType': 'mp3'
            }
        ],
        'code': 200
    }

请求响应中的 ``url`` ，即可下载到mp3文件。::

    import requests
    from nemcore.api import NetEaseApi

    box = NetEaseApi()
    # 取搜索结果的第一首歌
    song = box.search('戦姫絶唱')['result']['songs'][0]
    # 获取这首歌的下载链接
    resp = box.get_songs_url([song['id']])
    # 注意，由于没有登录，可能不能获得请求的320kbps高音质mp3
    mp3 = requests.get(resp['data'][0]['url'])
    # 最后将下载到的内容输出到文件
    # 也可以利用第三方库播放。
    fname = song['name']+'.mp3'
    with open(fname, 'w+b') as f:
        f.write(mp3.content)

接下来，我们可以使用本地播放器打开并播放。

.. image:: /images/tutorial/music.png

.. image:: /images/tutorial/play.png
