from Document import Document
from DataSource import DataSource
from BrowserDocument import BrowserDocument
from UI.LineInput import GetLineInput


class BrowserDataSource(DataSource):
    def __init__(self):
        super(DataSource, self).__init__()
        self._configed = False
        self._browser = ""

    def Configed(self):
        return self._configed

    def CreateDocument(self) -> Document:
        if not self._configed:
            return None
        return BrowserDocument(self._browser)

    def GetConfig(self)->str:
        browser, ret = GetLineInput("选择浏览器", "选择浏览器","可选浏览器：" + '，'.join(["Chrome", "Edge", "Firefox", "Ie", "Safari", "WebKitGTK", "WPEWebKit"]))
        if browser and ret:
            self.SetConfig(browser)
            return self._browser
        return None

    def SetConfig(self, browser:str):
        self._browser = browser
        self._configed = True
