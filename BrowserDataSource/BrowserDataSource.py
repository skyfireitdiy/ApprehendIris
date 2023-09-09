from Document import Document
from DataSource import DataSource
from BrowserDocument import BrowserDocument
from UI.Choice import GetChoice
from PyQt6.QtWidgets import QMessageBox


class BrowserDataSource(DataSource):
    def __init__(self):
        super(DataSource, self).__init__()
        self._configed = False
        self._browser = ""

    def Configed(self):
        return self._configed

    def CreateDocument(self) -> Document:
        if not self._configed:
            QMessageBox.critical(None, "错误", "数据源未配置")
            return None
        return BrowserDocument(self._browser)

    def GetConfig(self)->str:
        browser = GetChoice("选择浏览器", "浏览器",["Chrome", "Edge", "Firefox", "Ie", "Safari", "WebKitGTK", "WPEWebKit"])
        if browser:
            self.SetConfig(browser)
            return self._browser
        return None

    def SetConfig(self, browser:str):
        self._browser = browser
        self._configed = True

    def Description(self)->str:
        return  "从" + self._browser + "浏览器获取数据"
