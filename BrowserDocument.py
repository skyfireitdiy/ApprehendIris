from Document import Document, DocumentType
from selenium import webdriver
from newspaper import Article
import time
from bs4 import BeautifulSoup


class BrowserDocument(Document):
    driver = {
            "Chrome": webdriver.Chrome,
            "Edge": webdriver.Edge,
            "Firefox": webdriver.Firefox,
            "Ie": webdriver.Ie,
            "Safari": webdriver.Safari,
            "WebKitGTK": webdriver.WebKitGTK,
            "WPEWebKit": webdriver.WPEWebKit,
            }

    def __init__(self, browser):
        super().__init__(DocumentType.Browser)
        self.browser = browser
        if browser not in self.driver:
            raise Exception("Browser not supported")
        self.browser_inst = self.driver[browser]()

    def Read(self) -> str:
        try:
            ret = ""
            for h in self.browser_inst.window_handles:
                self.browser_inst.switch_to.window(h)
                page_source = self.browser_inst.execute_script("return document.documentElement.innerHTML")
                bs = BeautifulSoup(page_source, 'html.parser')
                ret += bs.get_text(separator=' ')
            return ret
        except Exception as e:
            print(e)
            self.browser_inst = self.driver[self.browser]()
            return ""


    def Name(self)->str:
        return "浏览器(" + self.browser + ")"

    def Cached(self) -> bool:
        return False
