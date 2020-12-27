# 快速开始

[nemcore](https://github.com/nnnewb/NEMCore) 是从
[netease-musicbox](https://github.com/darknessomi/musicbox/)
项目抽取的核心api模块，简化重构后的产物。

使用nemcore可以实现一个简单的网易云音乐播放器。

## 安装

你可以使用pip安装。:

    pip install nemcore

## 登录

使用 `nemcore.api.NetEaseApi.login`{.interpreted-text role="meth"} 接口登录。

登录信息会保存在cookie中，如需保存登录状态，可以在初始化
`nemcore.api.NetEaseApi`{.interpreted-text role="class"} 实例时传入
`cookie_path` 参数。

下次初始化 `nemcore.api.NetEaseApi`{.interpreted-text role="class"} 实例时会自动加载登录状态。

例子:

```python
from nemcore.api import NetEaseApi

box = NetEaseApi(cookie_path='./cookies')
box.login('cloudmusic@163.com', 'password')
print(box.uid)
```

上面的例子代码应该输出你的用户id。

如果登陆失败，上面的代码会抛出
`nemcore.exceptions.NetEaseError`{.interpreted-text role="class"} ，异常对象的 `code` 和 `message` 属性描述了错误的原因。

你还可以从`box.profile`属性获得当前用户的更多信息。:

```python
from nemcore.api import NetEaseApi

box = NetEaseApi(cookie_path='./cookies')
```

美化后的输出类似于下面的样子（内容已脱敏）：:

```json
{
  "mutual": false,
  "remarkName": null,
  "userType": 0,
  "djStatus": 0,
  "expertTags": null,
  "authStatus": 0,
  "experts": {},
  "followed": false,
  "backgroundUrl": "",
  "detailDescription": "",
  "vipType": 0,
  "gender": 0,
  "accountStatus": 0,
  "description": "",
  "defaultAvatar": true,
  "avatarImgId": 0,
  "nickname": "",
  "birthday": 0,
  "userId": 0,
  "backgroundImgId": 0,
  "avatarUrl": "",
  "province": 0,
  "city": 100,
  "backgroundImgIdStr": "",
  "avatarImgIdStr": "",
  "signature": "",
  "authority": 0,
  "avatarImgId_str": "",
  "followeds": 0,
  "follows": 3,
  "eventCount": 0,
  "avatarDetail": null,
  "playlistCount": 1,
  "playlistBeSubscribedCount": 0
}
```

## 登出

如果需要登出，可以调用 `nemcore.api.NetEaseApi.logout`{.interpreted-text role="meth"}。:

```python
from nemcore.api import NetEaseApi

box = NetEaseApi(cookie_path='./cookies')
box.login('nemcore@163.com', 'password')
box.logout()
```

登出后，磁盘上持久化的登录cookie会立即清除。

## 收藏的歌单

通过 `nemcore.api.NetEaseApi.get_user_playlist`{.interpreted-text role="meth"} 来获取用户的歌单清单:

```python
from nemcore.api import NetEaseApi

box = NetEaseApi(cookie_path='./cookies')
box.login('cloudmusic@163.com', 'password')

result = box.get_user_playlist()
```

结果如下（部分数据脱敏处理）:

```json
{
  "version": "1608025050267",
  "more": false,
  "playlist": [
    {
      "subscribers": [],
      "subscribed": false,
      "creator": {
        "defaultAvatar": true,
        "province": 440000,
        "authStatus": 0,
        "followed": false,
        "avatarUrl": "http://p1.music.126.net/RLeBJe4D1ZzUtltxfoKDMg==/109951163250239066.jpg",
        "accountStatus": 0,
        "gender": 0,
        "city": 440100,
        "birthday": -2209017600000,
        "userId": 0,
        "userType": 0,
        "nickname": "nemcore",
        "signature": "",
        "description": "",
        "detailDescription": "",
        "avatarImgId": 109951163250239066,
        "backgroundImgId": 109951162868128395,
        "backgroundUrl": "http://p1.music.126.net/2zSNIqTcpHL2jIvU6hG0EA==/109951162868128395.jpg",
        "authority": 0,
        "mutual": false,
        "expertTags": null,
        "experts": null,
        "djStatus": 0,
        "vipType": 0,
        "remarkName": null,
        "authenticationTypes": 0,
        "avatarDetail": null,
        "backgroundImgIdStr": "109951162868128395",
        "avatarImgIdStr": "109951163250239066",
        "anchor": false,
        "avatarImgId_str": "109951163250239066"
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
      "recommendInfo": null,
      "description": null,
      "tags": [],
      "status": 0,
      "trackNumberUpdateTime": 0,
      "adType": 0,
      "userId": 4008684819,
      "createTime": 1608025049340,
      "highQuality": false,
      "ordered": false,
      "subscribedCount": 0,
      "cloudTrackCount": 0,
      "updateTime": 1608025049340,
      "trackCount": 0,
      "commentThreadId": "A_PL_0_5381566010",
      "playCount": 0,
      "coverImgId": 109951165434984508,
      "coverImgUrl": "http://p4.music.126.net/9-rm4PUkKuL-lD1Rgg6SDw==/109951165434984508.jpg",
      "specialType": 5,
      "totalDuration": 0,
      "newImported": false,
      "anonimous": false,
      "privacy": 0,
      "trackUpdateTime": 1608025050561,
      "name": "我喜欢的音乐",
      "id": 0,
      "coverImgId_str": "109951165434984508"
    }
  ],
  "code": 200
}
```

对于有非常多歌单的，可以用 `offset` 和 `limit`
参数分页获取。这里不做更多说明了。

## 歌单详情

通过 `nemcore.api.NetEaseApi.get_playlist_detail`{.interpreted-text role="meth"} 获取歌单的详情。:

```python
from nemcore.api import NetEaseApi

box = NetEaseApi(cookie_path='./cookies')
box.login('cloudmusic@163.com', 'password')

result = box.get_user_playlist()
playlist = result['playlist'][2]
resp = box.get_playlist_detail(playlist['id'])
print(resp)
```

获取的歌单详情输出如下：:

```json
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
      }
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
      }
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
    }
  ]
}
```

## 日推歌单

通过 `nemcore.api.NetEaseApi.get_recommend_songs`{.interpreted-text role="meth"} 获取你的今日推荐。

需要登录才能调用，否则会出现错误代码 `301`。

参考下面的例子调用：:

```python
from nemcore.api import NetEaseApi

box = NetEaseApi()
result = box.get_recommend_songs()
```

最终输出不给例子了。

## 搜索

通过使用 `nemcore.api.NetEaseApi.search`{.interpreted-text role="meth"} 方法搜索歌曲，这个方法会返回一个歌曲清单。

```python
from nemcore.api import NetEaseApi

box = NetEaseApi()
box.search('战姬绝唱')
```

结果不做演示

## 下载mp3

通过 `nemcore.api.NetEaseApi.get_songs_url`{.interpreted-text role="meth"} 来获取歌曲播放链接。:

```python
from nemcore.api import NetEaseApi

box = NetEaseApi()
# 取搜索结果的第一首歌
song = box.search('戦姫絶唱')['result']['songs'][0]
# 获取这首歌的详情
resp = box.get_songs_url([song['id']])
```

结果不做展示。
