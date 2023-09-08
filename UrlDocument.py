from Document import Document, DocumentType
import requests
from bs4 import BeautifulSoup

class UrlDocument(Document):
    def __init__(self, url):
        super().__init__(DocumentType.Url)
        self._url = url

    def Read(self):
        response = requests.get(self._url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        return text

    def Name(self)->str:
        return self._url
