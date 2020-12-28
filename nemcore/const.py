from collections import OrderedDict

from nemcore.utils import random_jsession_id, random_nuid

HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com',
    'User-Agent': ' '.join([
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5)',
        'AppleWebKit/537.36 (KHTML, like Gecko)',
        'Chrome/59.0.3071.115 Safari/537.36',
    ]),
}

BASE_COOKIES = {
    'JSESSIONID-WYYY': random_jsession_id(),
    '_iuqxldmzr_': '32',
    # FIXME: key重复了，但确实可以工作，也解决了 -460 cheating 的问题。这部分要完善一下。
    '_ntes_nnid': random_nuid(),
    '_ntes_nuid': random_nuid(with_timestamp=False)
}

DEFAULT_TIMEOUT = 10
BASE_URL = 'http://music.163.com'

# 歌曲榜单地址
TOP_LIST_ALL = {
    0: ['云音乐新歌榜', '3779629'],
    1: ['云音乐热歌榜', '3778678'],
    2: ['网易原创歌曲榜', '2884035'],
    3: ['云音乐飙升榜', '19723756'],
    4: ['云音乐电音榜', '10520166'],
    5: ['UK排行榜周榜', '180106'],
    6: ['美国Billboard周榜', '60198'],
    7: ['KTV嗨榜', '21845217'],
    8: ['iTunes榜', '11641012'],
    9: ['Hit FM Top榜', '120001'],
    10: ['日本Oricon周榜', '60131'],
    11: ['韩国Melon排行榜周榜', '3733003'],
    12: ['韩国Mnet排行榜周榜', '60255'],
    13: ['韩国Melon原声周榜', '46772709'],
    14: ['中国TOP排行榜(港台榜)', '112504'],
    15: ['中国TOP排行榜(内地榜)', '64016'],
    16: ['香港电台中文歌曲龙虎榜', '10169002'],
    17: ['华语金曲榜', '4395559'],
    18: ['中国嘻哈榜', '1899724'],
    19: ['法国 NRJ EuroHot 30周榜', '27135204'],
    20: ['台湾Hito排行榜', '112463'],
    21: ['Beatport全球电子舞曲榜', '3812895'],
    22: ['云音乐ACG音乐榜', '71385702'],
    23: ['云音乐嘻哈榜', '991319590']
}

PLAYLIST_CLASSES = OrderedDict([
    (
        '语种',
        [
            '华语',
            '欧美',
            '日语',
            '韩语',
            '粤语',
            '小语种',
        ],
    ),
    (
        '风格',
        [
            '流行',
            '摇滚',
            '民谣',
            '电子',
            '舞曲',
            '说唱',
            '轻音乐',
            '爵士',
            '乡村',
            'R&B/Soul',
            '古典',
            '民族',
            '英伦',
            '金属',
            '朋克',
            '蓝调',
            '雷鬼',
            '世界音乐',
            '拉丁',
            '另类/独立',
            'New Age',
            '古风',
            '后摇',
            'Bossa Nova',
        ],
    ),
    (
        '场景',
        [
            '清晨',
            '夜晚',
            '学习',
            '工作',
            '午休',
            '下午茶',
            '地铁',
            '驾车',
            '运动',
            '旅行',
            '散步',
            '酒吧',
        ],
    ),
    (
        '情感',
        [
            '怀旧',
            '清新',
            '浪漫',
            '性感',
            '伤感',
            '治愈',
            '放松',
            '孤独',
            '感动',
            '兴奋',
            '快乐',
            '安静',
            '思念',
        ],
    ),
    (
        '主题',
        [
            '影视原声',
            'ACG',
            '儿童',
            '校园',
            '游戏',
            '70后',
            '80后',
            '90后',
            '网络歌曲',
            'KTV',
            '经典',
            '翻唱',
            '吉他',
            '钢琴',
            '器乐',
            '榜单',
            '00后',
        ],
    ),
])
