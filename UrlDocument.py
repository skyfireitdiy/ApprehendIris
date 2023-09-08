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
        paragraphs = soup.find_all('p')
        text = '\n'.join([p.text for p in paragraphs])
        return text

    def Name(self)->str:
        return self._url
