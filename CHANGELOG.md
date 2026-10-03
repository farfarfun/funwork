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
- `item_utils.fill_item_info`/`fill_item_info_dict` 的 `urllib3` 请求补上超时，避免网络
  异常时无限等待。
- `youzan.dubbo_client.Dubbo.get_dubbo_result` 的 `requests.post` 补上超时与
  `raise_for_status`，请求或响应解析失败时抛出带接口地址上下文的 `RuntimeError`
  （而不是让底层异常或错误状态码的响应体直接透传）。
- 修复 `fill_item_info_dict` 在列表中存在缺失 `itemId` 的字典时抛出 `KeyError` 的问题
  （合并结果阶段未使用与筛选阶段一致的安全取值方式）。
- 移除模块内遗留的未使用调试函数 `_legacy_test_removed`/`_legacy_test2_removed`
  （内嵌真实商品 ID 的死代码，从未被调用）。
