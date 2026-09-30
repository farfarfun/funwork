"""funwork 公开 API 测试。"""

import datetime

import pandas as pd
import pytest
import requests

from funwork import item_utils
from funwork.youzan import items
from funwork.youzan.dubbo_client import Dubbo
from funwork.youzan.pdf_to_html import DataFrameToHtml


class Response:
    def __init__(self, payload=None, text=""):
        self.payload = payload
        self.text = text

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_import():
    import funwork

    assert funwork is not None


def test_fill_item_info(monkeypatch):
    response = {"result": {"result": [{"itemId": "1", "price": {"price": 12}}]}}
    monkeypatch.setattr(
        item_utils.urllib3.PoolManager,
        "request",
        lambda self, method, url: type(
            "R", (), {"data": item_utils.demjson.encode(response)}
        )(),
    )
    assert item_utils.fill_item_info(["1"])[0]["price"] == 12


@pytest.mark.parametrize("value", [None, "1"])
def test_fill_item_info_rejects_non_list(value):
    with pytest.raises(TypeError):
        item_utils.fill_item_info(value)


def test_fill_item_info_dict_merges_results(monkeypatch):
    response = {"result": {"result": [{"itemId": "1", "price": {"price": 12}}]}}
    monkeypatch.setattr(
        item_utils.urllib3.PoolManager,
        "request",
        lambda self, method, url: type(
            "R", (), {"data": item_utils.demjson.encode(response)}
        )(),
    )
    assert item_utils.fill_item_info_dict([{"itemId": "1"}])[0]["price"] == 12


def test_dataframe_to_html_escapes_content_and_links():
    frame = pd.DataFrame(
        [{"id": "<1>", "url": 'https://example.test/?a="x"', "image": "x&y"}]
    )
    html = DataFrameToHtml(frame).html_str()
    assert "&lt;1&gt;" in html
    assert "&quot;x&quot;" in html
    assert "x&amp;y?w=250&amp;h=250&amp;cp=1" in html
    assert "<th>url</th>" not in html


def test_dataframe_to_html_handles_empty_frame():
    html = DataFrameToHtml(pd.DataFrame(columns=["id"])).html_str()
    assert "<tr><th>id</th></tr>" in html


def test_dubbo_posts_encoded_data(monkeypatch):
    seen = {}

    def post(url, headers, data):
        seen.update(url=url, headers=headers, data=data)
        return Response(text='{"ok": true}')

    monkeypatch.setattr("funwork.youzan.dubbo_client.requests.post", post)
    result = Dubbo("https://host", "service", "method").get_dubbo_result({"id": 1})
    assert result == {"ok": True}
    assert seen["url"] == "https://host/soa/service/method"


def test_get_data_from_console_and_request_error(monkeypatch):
    monkeypatch.setattr(
        items.requests, "get", lambda url, timeout: Response({"data": 1})
    )
    assert items.get_data_from_console("https://example.test") == {"data": 1}

    def fail(url, timeout):
        raise requests.RequestException("offline")

    monkeypatch.setattr(items.requests, "get", fail)
    with pytest.raises(RuntimeError, match="请求数据失败"):
        items.get_data_from_console("https://example.test")


def test_get_item_detail(monkeypatch):
    monkeypatch.setattr(items, "_secret", lambda *args: "https://example.test/{}/{}")
    monkeypatch.setattr(
        items, "get_data_from_console", lambda url: {"data": {"id": url}}
    )
    assert items.get_item_detail("1", "2") == {"id": "https://example.test/1/2"}

    monkeypatch.setattr(items, "get_data_from_console", lambda url: [])
    with pytest.raises(TypeError, match="响应必须是对象"):
        items.get_item_detail("1", "2")


def test_get_data_from_dp_ready_and_pending(monkeypatch):
    monkeypatch.setattr(items, "_secret", lambda name, *args: name)
    payload = {
        "data": {
            "completed": True,
            "metaData": [
                {"columnName": "count", "columnType": "bigint"},
                {"columnName": "ratio", "columnType": "float"},
            ],
            "queryResult": [["2", "1.5"]],
        }
    }
    monkeypatch.setattr(
        items.requests, "get", lambda *args, **kwargs: Response(payload)
    )
    frame = items.get_data_from_dp("key")
    assert isinstance(frame, pd.DataFrame)
    assert frame.iloc[0].to_dict() == {"count": 2.0, "ratio": 1.5}

    payload["data"]["completed"] = False
    assert items.get_data_from_dp("key") == "not ready"


def test_get_day(monkeypatch):
    class FixedDateTime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 9, 30, tzinfo=tz)

    monkeypatch.setattr(items.datetime, "datetime", FixedDateTime)
    assert items.get_day(1) == "20260929"
