# 贡献指南 (Contributing Guide)

感谢你考虑为本项目做出贡献！

### 开发环境配置
本项目使用 [uv](https://github.com/astral-sh/uv) 进行管理：
1. Fork 并克隆仓库。
2. 安装依赖：`uv sync`。
3. 所有的开发工具（Ruff, Pytest）都已包含在内。

### 代码标准
我们使用 **Ruff** 来保持代码整洁。在提交 PR 之前，请务必运行：
- 检查逻辑：`uv run ruff check --fix .`
- 格式化：`uv run ruff format .`

### 提交 PR 流程
1. 创建功能分支 (`git checkout -b feature/amazing-feature`)。
2. 提交更改 (`git commit -m 'Add some amazing feature'`)。
3. 推送到分支 (`git push origin feature/amazing-feature`)。
4. 开启一个 Pull Request。