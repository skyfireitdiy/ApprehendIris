from Document import Document
from DataSource import DataSource
from UI.LineInput import GetLineInput
from UrlDocument import UrlDocument


class UrlDataSource(DataSource):
    def __init__(self) -> None:
        super().__init__()

    def CreateDocument(self) -> Document:
        url, ret = GetLineInput("输入", "请输入URL")
        if ret and url:
            return UrlDocument(url)
        return None

    def Configed(self):
        return True

    def Description(self)->str:
        return "从URL获取数据"
