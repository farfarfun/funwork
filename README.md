# funwork

工作用零散脚本集合：批量查询微店商品信息（`item_utils`）、通过 HTTP 网关泛化调用有赞
Dubbo 服务（`youzan.dubbo_client`）、查询有赞商品/数据平台接口（`youzan.items`）、将
`pandas.DataFrame` 渲染成 HTML 报表（`youzan.pdf_to_html`，不处理 PDF 文件）。网络接口
凭据不会写入源码，运行前请通过环境变量或 `funsecret` 配置。

## 安装

```bash
uv add funwork
```

## 最小示例

```python
import pandas as pd
from funwork.youzan.pdf_to_html import DataFrameToHtml

html = DataFrameToHtml(
    pd.DataFrame([{"id": 1, "url": "https://example.com"}])
).html_str()
assert "example.com" in html
```

## 配置网络接口

设置 `FUNWORK_ITEM_DETAIL_URL`（支持 `{}` 两个格式化参数）、`FUNWORK_DP_URL`、
`FUNWORK_DP_AUTHORIZATION` 和 `FUNWORK_DP_COOKIE`，或将相同配置写入 `funsecret`。

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
