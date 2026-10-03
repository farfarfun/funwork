from typing import TypeAlias

import demjson3 as demjson
import urllib3
from farlog import getLogger

logger = getLogger("funwork.item_utils")

__all__ = ["fill_item_info", "fill_item_info_dict"]


_REQUEST_TIMEOUT = 30.0

JsonValue: TypeAlias = (
    None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
)


def fill_item_info(item_list: list[str] | None = None) -> list[dict[str, JsonValue]]:
    """按商品 ID 批量查询微店商品详情（含价格）。

    Args:
        item_list: 商品 ID 字符串列表，不能为 ``None`` 或非列表类型。

    Returns:
        每个商品的详情字典列表，额外附带 ``priceInfo``（原始价格对象）和
        ``price``（展开后的价格数值）字段。

    Raises:
        TypeError: ``item_list`` 为 ``None`` 或不是列表时抛出。
        KeyError: 接口响应缺少 ``result``/``price`` 等预期字段时抛出。
    """
    if item_list is None or not isinstance(item_list, list):
        raise TypeError("item_list 必须是列表")
    items = ",".join(item_list)
    url = "http://pluto.vdian.net/solution/query?solutionId=1004&itemIdList=" + items

    r = urllib3.PoolManager().request("GET", url, timeout=_REQUEST_TIMEOUT)

    logger.debug("url:" + url)

    response = demjson.decode(r.data)

    logger.debug("response:" + str(response))
    result = response["result"]["result"]
    for res in result:
        res["priceInfo"] = res["price"]
        res["price"] = res["priceInfo"]["price"]
    return result


def fill_item_info_dict(
    item_list: list[dict[str, JsonValue]] | None = None,
) -> list[dict[str, JsonValue]]:
    """按 ``itemId`` 批量查询商品详情并原地合并回输入字典。

    Args:
        item_list: 待补全的商品字典列表，每个字典可选带 ``itemId`` 键；
            缺少或为 ``None`` 的 ``itemId`` 会被跳过、不发起查询。

    Returns:
        合并了查询结果的 ``item_list``（原地修改后原样返回）；缺少
        ``itemId`` 或查询无命中的条目保持不变。

    Raises:
        TypeError: ``item_list`` 为 ``None`` 或不是列表时抛出。
        KeyError: 接口响应缺少 ``result``/``price`` 等预期字段时抛出。
    """
    if item_list is None or not isinstance(item_list, list):
        raise TypeError("item_list 必须是列表")

    item_ids = set()

    for item in item_list:
        if "itemId" not in item or item["itemId"] is None:
            continue
        item_ids.add(item["itemId"])

    items = ",".join(item_ids)
    url = "http://pluto.vdian.net/solution/query?solutionId=1004&itemIdList=" + items

    r = urllib3.PoolManager().request("GET", url, timeout=_REQUEST_TIMEOUT)

    logger.debug("url:" + url)

    response = demjson.decode(r.data)

    logger.debug("response:" + str(response))
    result = response["result"]["result"]

    res_map = {}
    for res in result:
        res["priceInfo"] = res["price"]
        res["price"] = res["priceInfo"]["price"]
        res_map[str(res["itemId"])] = res

    for item in item_list:
        item.update(res_map.get(item.get("itemId"), {}))

    return item_list
