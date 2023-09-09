from Document import Document
from DataSource import DataSource
from BrowserDocument import BrowserDocument


class BrowserDataSource(DataSource):
    def __init__(self):
        super(DataSource, self).__init__()

        self._configed = True

    def Configed(self):
        return self._configed

    def CreateDocument(self) -> Document:
        if not self._configed:
            return None
        return BrowserDocument("Edge", "https://www.baidu.com")
