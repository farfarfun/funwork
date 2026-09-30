# funwork

有赞商品接口和 HTML 报表工具。网络接口凭据不会写入源码，运行前请通过环境变量或 `funsecret` 配置。

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
