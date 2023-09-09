from Document import Document, DocumentType
from selenium import webdriver
from newspaper import Article


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

    def __init__(self, browser, start_url):
        super().__init__(DocumentType.Browser)
        self.browser = browser
        self.start_url = start_url
        if browser not in self.driver:
            raise Exception("Browser not supported")
        self.browser_inst = self.driver[browser]()
        self.browser_inst.get(self.start_url)

    def Read(self) -> str:
        print(self.browser_inst.window_handles)
        page_source = self.browser_inst.page_source
        article = Article("")
        article.set_html(page_source)
        article.parse()
        return f"作者：{article.authors}\n标题：{article.title}\n发布时间：{article.publish_date}\n内容：{article.text}\n"

    def Name(self)->str:
        return "浏览器(" + self.browser + ")"

    def Cached(self) -> bool:
        return False