from Document import Document, DocumentType

class PlainTextDocument(Document):
    def __init__(self, text):
        super().__init__(DocumentType.PlainText)
        self.text = text
        
    def Read(self):
        return self.text

    def Name(self):
        return "纯文本"
