from typing import Any

import demjson3 as demjson
import urllib3
from farlog import getLogger

logger = getLogger("funwork.item_utils")

__all__ = ["fill_item_info", "fill_item_info_dict"]


_REQUEST_TIMEOUT = 30.0


def fill_item_info(item_list: list[str] | None = None) -> list[dict[str, Any]]:
    """根据商品 ID 查询商品信息。"""
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
    item_list: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """把查询到的商品信息合并到商品字典列表。"""
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
