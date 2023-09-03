from Document import Document, DocumentType
import docx2txt

class DocDocument(Document):
    def __init__(self, doc_file_path):
        super().__init__(DocumentType.Doc)
        self._doc_file_path = doc_file_path

    def Read(self):
        return docx2txt.process(self._doc_file_path)

    def Name(self)->str:
        return self._doc_file_path
