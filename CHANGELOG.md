# 更新日志

## [Unreleased] - 2026-08-28

### 变更

- **破坏性变更：** 将包从 `notework` 重命名为 `funwork`。迁移方法：
  GitHub repository name. The import name and the PyPI distribution name both change:
  - `import notework` -> `import funwork`
  - `pip install notework` -> `pip install funwork`
- 将导入从 `notework` 改为 `funwork`，并将安装命令从 `pip install notework` 改为
  `pip install funwork`。`notework` 未发布，无需兼容转发包。

### 修复

- 移除源码中的硬编码凭据，并补齐运行时依赖声明。
