from Document import Document
from DataSource import DataSource
from PlainTextDocument import PlainTextDocument
from UI.PlainTextInput import GetPlainTextInput

class PlainTextDataSource(DataSource):
    def __init__(self) -> None:
        super().__init__()

    def CreateDocument(self) -> Document:
        text, ret = GetPlainTextInput("输入", "请输入文本")
        if text and ret:
            return PlainTextDocument(text)
        return None

    def Configed(self):
        return True

    def Description(self) -> str:
        return "输入纯文本"
