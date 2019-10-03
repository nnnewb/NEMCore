# NetEase Cloud Music ApiClient

网易云音乐核心 API 客户端。

这个项目的目的是抽离一个干净的 API Client，便于二次开发和维护。

主要代码来自[NetEase-MusicBox](https://github.com/darknessomi/musicbox/)，非常感谢每一位该项目的贡献者。

## 后续计划

- [x]添加测试用例
- [ ]规范命名和返回值结构
- [ ]提供助手函数，实现一些常用操作
- [ ]移除 python2 支持(`__future__`等)，迁移到 python3.6+
- [ ]支持异步(考虑`aiohttp`)
