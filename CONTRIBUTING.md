# 参与 nemcore 开发

这是我个人出于兴趣和学习的目的开的项目，鉴于项目本身处于灰色地带，不欢迎任何公开的宣传布道活动。当然我也拦不住你，总而言之，**别干**。谢谢。

参与开发的方式有几种：

- 提 issue。bug，code review，新点子，上游 api 变了之类的问题。
- 提 pull request，注意遵守代码规范，说明 pr 要解决的问题。

## 规范/约定

1. 项目使用`setuptools`管理依赖，暂不考虑 `pyproject.toml` ，除非 pip 支持完善或 poetry 等工具成为 python 默认分发的包管理工具。
2. commit message 格式没有强制要求，但最好能符合一般格式，每个 commit 有明确的主题，便于 review。
   如果提交的代码很多又没有明确的 commit message 可能会被拒绝合并。
3. 最好能自己做一下 flake8 或者 pylint 的检查。
4. 推荐用 yapf 格式化一下代码再提交。
5. 添加或修改 api 注意留个测试。
6. 有 breaking change 或者比较多的修改可以先提个 issue 讨论下，避免做无用功。
7. 不要提交 ide/编辑器的配置，如`.vscode`

其他想到再说。
