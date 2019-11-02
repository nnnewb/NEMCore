# NetEase Cloud Music ApiClient

<!-- badges -->

![python-version](https://img.shields.io/pypi/pyversions/nemcore)
![pypi-version](https://img.shields.io/pypi/v/nemcore)
[![Documentation Status](https://readthedocs.org/projects/nemcore/badge/?version=latest)](https://nemcore.readthedocs.io/en/latest/?badge=latest)
![github-issues](https://img.shields.io/github/issues-raw/nnnewb/nemcore)
![license](https://img.shields.io/github/license/nnnewb/nemcore)
![downloads](https://img.shields.io/pypi/dd/nemcore)

<!-- badges/ -->

网易云音乐核心 API 客户端。

这个项目的目的是抽离一个干净的 API Client，便于二次开发和维护。

主要代码来自[NetEase-MusicBox](https://github.com/darknessomi/musicbox/)，非常感谢每一位该项目的贡献者。

**警告，目前 API 尚未稳定，不保证兼容性。万一有新点子说不定就会改。**

此外欢迎 code review 和 pull request。

## 使用方法

### quickstart

```python
from nemcore.api import NetEaseApi

netease = NetEaseApi(cookie_path='./cookies')
netease.login('cloudmusic@163.com', 'password')

# 获取我的歌单
playlists = netease.get_user_playlist()

# 获取日推
recommend = netease.get_recommend_songs()

# 签到
netease.daily_task()
```

详细的 api 文档和快速开始请参考[这里](https://nemcore.readthedocs.io/en/latest/)。

## v1.0 开发计划

- [x] 添加测试用例
- [x] 规范命名和返回值结构
- [x] 提供可配置的缓存(是否持久化，缓存有效时间等)
- [x] 提供文档，挂在[readthedocs.io](https://nemcore.readthedocs.io/en/latest/)上。
- [x] 重构简化 api 和实现。
- [ ] 提供助手函数，实现一些常用操作
- [x] 移除 python2 支持(`__future__`等)，迁移到 python3.6+
- [ ] 支持异步(考虑`aiohttp`)

## changelog

### 0.1.4

本版本主要是对代码进行重构，将核心 Api 类清晰化，解耦无关逻辑，简化了使用。

此外，提供了比较详细的入门文档，帮助使用者快速了解使用方式和 api 的响应内容。

不过 api 文档不是很好，需要改进。

- `nemcore.netease` 模块重命名成 `nemcore.api`
- `nemcore.netease.NetEase` 重命名成 `nemcore.api.NetEaseApi`
- 删除 `nemcore.conf` 模块
- 删除 `nemcore.storage` 模块
- 删除 `nemcore.parser` 模块
- 删除 `nemcore.pdict` 模块
- 添加 sphinx 文档和快速开始指引，文档已经挂到了 readthedocs.io

### 0.1.3

- 支持缓存。基于`pickle`和`cachetools`实现，可配置缓存时间和是否持久化
