# NetEase Cloud Music ApiClient

<!-- badges -->

![python-version](https://img.shields.io/pypi/pyversions/nemcore)
![pypi-version](https://img.shields.io/pypi/v/nemcore)
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
from nemcore.netease import NetEase

netease = NetEase()
netease.login('mail@163.com', 'password')

# 获取我的歌单
playlists = netease.get_user_playlist()

# 获取日推
recommend = netease.get_recommend_songs()

# 签到
netease.daily_task()
```

其他 API 文档待补充。

## v1.0 开发计划

- [x] 添加测试用例
- [x] 规范命名和返回值结构
- [x] 提供可配置的缓存(是否持久化，缓存有效时间等)
- [ ] 提供助手函数，实现一些常用操作
- [ ] 移除 python2 支持(`__future__`等)，迁移到 python3.6+
- [ ] 支持异步(考虑`aiohttp`)

## changelog

### 0.1.3

- 支持缓存。基于`pickle`和`cachetools`实现，可配置缓存时间和是否持久化
