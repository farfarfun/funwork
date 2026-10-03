"""有赞商品和数据平台接口。凭据只从环境变量或 funsecret 读取。"""

import datetime
import json
import os
from typing import TypeAlias

import numpy as np
import pandas as pd
import requests
from farlog import getLogger

logger = getLogger("funwork.youzan.items")

JsonValue: TypeAlias = (
    None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
)


class ConfigurationError(RuntimeError):
    """接口凭据未配置。"""


def _secret(env_name: str, *category: str) -> str:
    value = os.getenv(env_name)
    if value:
        return value
    try:
        from funsecret import read_secret

        value = read_secret(*category)
    except (ImportError, OSError, RuntimeError):
        value = None
    if value:
        return value
    raise ConfigurationError(f"未配置 {env_name}，请设置环境变量或写入 funsecret")


def get_data_from_console(url: str) -> JsonValue:
    """请求 JSON 接口并返回解码后的数据。

    Args:
        url: 完整的请求地址（含查询参数），使用 GET 方法请求。

    Returns:
        响应体解码后的 JSON 值。

    Raises:
        RuntimeError: 请求失败、响应状态非 2xx 或响应体不是合法 JSON 时抛出，
            携带请求地址上下文，并保留原始异常。
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        raise RuntimeError(f"请求数据失败: {url}") from exc


def get_item_detail(item_id: str, shop_id: str) -> JsonValue:
    """查询有赞商品详情。

    Args:
        item_id: 商品 ID。
        shop_id: 店铺 ID。

    Returns:
        响应体 ``data`` 字段对应的 JSON 值（可能为 ``None``）。

    Raises:
        ConfigurationError: 未配置 ``FUNWORK_ITEM_DETAIL_URL`` 时抛出。
        RuntimeError: 底层请求失败时抛出（见 `get_data_from_console`）。
        TypeError: 接口响应不是 JSON 对象时抛出。
    """
    template = _secret(
        "FUNWORK_ITEM_DETAIL_URL", "funwork", "youzan", "item_detail_url"
    )
    result = get_data_from_console(template.format(item_id, shop_id))
    if not isinstance(result, dict):
        raise TypeError("商品详情接口响应必须是对象")
    return result.get("data")


def get_data_from_dp(key: str = "201912091501484e6f5230") -> pd.DataFrame | str:
    """按查询 key 读取有赞数据平台的查询结果并转换为 DataFrame。

    Args:
        key: 数据平台查询任务的标识。

    Returns:
        查询已完成时返回按 ``metaData`` 列类型转换好的 `pandas.DataFrame`
        （``bigint`` 转 ``int64``、``float`` 转 ``float64``）；查询尚未完成
        （``completed`` 为假）时返回字符串 ``"not ready"``。

    Raises:
        ConfigurationError: 未配置 ``FUNWORK_DP_URL``/``FUNWORK_DP_AUTHORIZATION``/
            ``FUNWORK_DP_COOKIE`` 时抛出。
        RuntimeError: 底层请求失败或响应不是合法 JSON 时抛出，携带请求地址
            上下文，并保留原始异常。
        KeyError: 响应缺少 ``data``/``completed``/``metaData`` 等预期字段时抛出。
    """
    base_url = _secret("FUNWORK_DP_URL", "funwork", "youzan", "dp_url")
    authorization = _secret(
        "FUNWORK_DP_AUTHORIZATION", "funwork", "youzan", "dp_authorization"
    )
    cookie = _secret("FUNWORK_DP_COOKIE", "funwork", "youzan", "dp_cookie")
    try:
        response = requests.get(
            base_url + key,
            headers={
                "Authorization": authorization,
                "Content-Type": "application/json",
                "Cookie": cookie,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        raise RuntimeError(f"数据平台请求失败: {base_url}") from exc
    if not data["data"]["completed"]:
        return "not ready"
    metadata = data["data"]["metaData"]
    columns = [column["columnName"] for column in metadata]
    frame = pd.DataFrame(data["data"]["queryResult"], columns=columns)
    for column, info in zip(columns, metadata):
        if info["columnType"] == "bigint":
            frame[column] = frame[column].astype(np.int64)
        elif info["columnType"] == "float":
            frame[column] = frame[column].astype(np.float64)
    return frame


def get_day(day: int = 1, fm: str = "%Y%m%d") -> str:
    """返回距今天（UTC）指定天数之前的日期字符串。

    Args:
        day: 向前推移的天数，默认 1（即昨天）。
        fm: `datetime.strftime` 格式串，默认 ``"%Y%m%d"``。

    Returns:
        按 `fm` 格式化后的日期字符串。
    """
    today = datetime.datetime.now(datetime.timezone.utc).date()
    return (today - datetime.timedelta(days=day)).strftime(fm)
