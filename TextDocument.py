from Document import Document, DocumentType

class TextDocument(Document):
    def __init__(self, text_file_path):
        super().__init__(DocumentType.Text)
        self._text_file_path = text_file_path
        
    def Read(self)->str:
        with open(self._text_file_path, 'r') as f:
            return f.read()

    def Name(self)->str:
        return self._text_file_path


