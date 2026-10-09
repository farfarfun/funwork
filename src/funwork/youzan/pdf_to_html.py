"""把 pandas DataFrame 渲染为 HTML 表格。"""

from html import escape

import pandas as pd


class DataFrameToHtml:
    """把 pandas DataFrame 渲染为商品 HTML 表格。"""

    def __init__(self, data: pd.DataFrame) -> None:
        """从 DataFrame 初始化表格列和记录。

        Args:
            data: 要渲染的数据表；`url` 列仅用于为 `id` 列生成链接。
        """
        self.columns = list(data.columns)
        self.data_dict = data.to_dict(orient="records")
        self.pass_words = {"url"}

    def html_str(self) -> str:
        """返回转义后的 HTML 表格。"""
        columns = [column for column in self.columns if column not in self.pass_words]
        head = (
            "<tr>"
            + "".join(f"<th>{escape(str(column))}</th>" for column in columns)
            + "</tr>"
        )
        rows = []
        for row in self.data_dict:
            cells = []
            for column in columns:
                value = escape(str(row.get(column, "")))
                if column == "id" and row.get("url"):
                    value = f'<a href="{escape(str(row["url"]), quote=True)}" target="_blank">{value}</a>'
                elif "img" in column or "image" in column:
                    image_url = f"{row.get(column, '')}?w=250&h=250&cp=1"
                    value = f'<img src="{escape(image_url, quote=True)}">'
                cells.append(f"<td>{value}</td>")
            rows.append("<tr>" + "".join(cells) + "</tr>")
        return "<html><body><table>" + head + "".join(rows) + "</table></body></html>"


pd2html = DataFrameToHtml
