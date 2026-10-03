from typing import TypeAlias

import demjson3 as demjson
import requests

JsonValue: TypeAlias = (
    None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
)


_REQUEST_TIMEOUT = 30.0


class Dubbo:
    """调用有赞 Dubbo HTTP 转发接口。"""

    def __init__(self, tether_host: str, interface: str, method: str) -> None:
        self.tether_host = tether_host
        self.interface = interface
        self.method = method

    def get_dubbo_result(self, data: dict[str, JsonValue]) -> JsonValue:
        """发送请求并返回解码后的响应。

        Args:
            data: 透传给 Dubbo 方法的参数。

        Returns:
            解码后的 JSON 响应。

        Raises:
            RuntimeError: 请求失败、响应状态非 2xx 或响应体无法解析时抛出，
                携带接口地址上下文，并保留原始异常。
        """
        headers = {"Content-Type": "application/json", "X-Request-Protocol": "dubbo"}
        payload = demjson.encode(data)
        url = f"{self.tether_host}/soa/{self.interface}/{self.method}"
        try:
            response = requests.post(
                url, headers=headers, data=payload, timeout=_REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return demjson.decode(response.text)
        except requests.RequestException as exc:
            raise RuntimeError(f"Dubbo 请求失败: {url}") from exc
        except demjson.JSONDecodeError as exc:
            raise RuntimeError(f"Dubbo 响应解析失败: {url}") from exc


dubbo = Dubbo
