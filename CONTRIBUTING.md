# 参与 nemcore 开发

这是我个人出于兴趣和学习的目的开的项目，鉴于项目本身处于灰色地带，不欢迎任何公开的宣传布道活动。当然我也拦不住你，总而言之，**别干**。谢谢。

参与开发的方式有几种：

- 提 issue。bug，code review，新点子，上游 api 变了之类的问题。
- 提 pull request，注意遵守代码规范，说明 pr 要解决的问题。

## 规范/约定

1. 项目使用`poetry`管理依赖，请注意用`poetry add` 和`poetry add -D`添加依赖。
2. commit message 没有强制要求，但最好使用 `commitizen` 一类的工具来生成规范的提交信息，每个提交有明确的主题。
   如果提交的代码很多又没有明确的 commit message 可能会被拒绝合并。
3. 注意提交前使用`flake8`和`isort`检查代码是否存在未解决的问题。提示警告的地方应处理或显式注明 noqa，注释说明原因。
   `flake8`使用的插件:`flake8-bugbear`。使用`isort -rc -c nemcore`来检查`import`语句的顺序和格式。配置文件在项目根目录下可以找到。
4. 提交前使用`yapf`格式化代码。如果`yapf`格式化出来的效果很差，用`yapf: disable`和`yapf: enable`来关闭指定代码块的格式化。
5. 添加或修改 api 务必先确认单元测试没问题。
6. 如果预期会有较大规模的代码改变或 breaking change 务必先提 issue 。
7. 不要提交 ide/编辑器的配置，如`.vscode`

其他待补充。
