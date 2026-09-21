import demjson3 as demjson
import requests


class Dubbo:
    """调用有赞 Dubbo HTTP 转发接口。"""

    def __init__(self, tether_host: str, interface: str, method: str) -> None:
        self.tether_host = tether_host
        self.interface = interface
        self.method = method

    def get_dubbo_result(self, data: dict) -> dict:
        """发送请求并返回解码后的响应。"""
        headers = {"Content-Type": "application/json", "X-Request-Protocol": "dubbo"}
        data = demjson.encode(data)
        url = f"{self.tether_host}/soa/{self.interface}/{self.method}"
        response = requests.post(url, headers=headers, data=data)
        return demjson.decode(response.text)


dubbo = Dubbo
