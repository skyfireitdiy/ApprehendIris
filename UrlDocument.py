from Document import Document, DocumentType
import requests
from newspaper import Article

class UrlDocument(Document):
    def __init__(self, url):
        super().__init__(DocumentType.Url)
        self._url = url

    def Read(self):
        article = Article(url=self._url, language='zh')
        article.download()
        article.parse()
        return f"作者：{article.authors}\n标题：{article.title}\n发布时间：{article.publish_date}\n内容：{article.text}\n"

    def Name(self)->str:
        return self._url

