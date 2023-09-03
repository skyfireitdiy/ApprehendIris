from Document import Document, DocumentType
import PyPDF2

class PdfDocument(Document):
    def __init__(self,pdf_file_path):
        super().__init__(DocumentType.Pdf)
        self._pdf_file_path = pdf_file_path

    def Read(self):
        pdfFileObj = open(self._pdf_file_path, 'rb')
        reader = PyPDF2.PdfReader(pdfFileObj)
        text = []
        for page in reader.pages:
            text.append(page.extract_text())
        return '\n'.join(text)
