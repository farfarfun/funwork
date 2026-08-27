# funwork

一组作者本人对接有赞（Youzan）电商后台的私有自动化脚本合集：通过有赞的 Dubbo SOA 接口（HTTP+JSON 转发）查询商品/价格信息、把商品数据渲染成 HTML 报表，外加一个从内部数据平台拉取数据的脚本（`youzan/items.py`，鉴权信息以 Fernet 密文硬编码在代码里，只有拥有对应密钥的作者本人能用）。不是通用工具库，其他人无法直接复用。

> 注意：包名/导入名是 `notework`（历史 `note*` 命名遗留，见 [NAMING.md](https://github.com/farfarfun/todo-list/blob/master/NAMING.md)），与仓库名 `funwork` 不一致。经查 PyPI 上目前**没有**发布 `notework` 这个包（404，之前 README 里写的 `pip install notework` 已经失效）。PyPI 上确实存在一个叫 `funwork`（0.0.1）的包，但经核对其 wheel 内容只有一个空的 `funapi/__init__.py`，是历史上批量占位发布的空包，**和这个仓库的代码毫无关系**，请不要 `pip install funwork` 来使用本仓库的功能。

## 安装

PyPI 上没有可用的发布包，需要从源码安装：

```bash
git clone https://github.com/farfarfun/funwork.git
cd funwork
pip install -e .
```

（原 README 里的 `pip install git+https://github.com/notechats/notework.git` 地址也已过时，`notechats` 组织已迁移到 `farfarfun`。）

## 用法示例

### 调用有赞 Dubbo 接口

```python
from notework.youzan.dubbo import dubbo

d = dubbo(tether_host='http://your-tether-host', interface='xxx.xxx.Service', method='xxxMethod')
result = d.get_dubbo_result({'param': 'value'})
```

### 商品数据转 HTML 报表

```python
from notework.youzan.pdf2html import pd2html
import pandas as pd

df = pd.DataFrame([{'id': 1, 'url': 'https://...', 'image': 'https://...'}])
html_str = pd2html(df).html_str()
```

## 已知局限（如实说明）

- `notework/ItemUtils.py` 里的 `fill_item_info` 读取 `r.data_mock`，但 `urllib3` 的响应对象并没有 `data_mock` 这个属性（正常应为 `r.data`），这个函数实际运行会报错，属于遗留 bug，本次只做文档说明，不在本次改动范围内修复。
- `notework/youzan/items.py` 里的接口地址、鉴权 Token、Cookie 都是作者本人的加密凭据，外部使用者无法直接调用。
- 整体是 2019 年前后的个人工作脚本合集，未做后续维护，直接复用前请自行评估可用性。
