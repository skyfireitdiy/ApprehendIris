from DataSource import DataSource
from Document import Document
from DocDocument import DocDocument
from PdfDocument import PdfDocument
from TextDocument import TextDocument
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class FileDataSource(DataSource):
    def __init__(self) -> None:
        super().__init__()

    def CreateDocument(self) -> Document:
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilters(
            ["文本文件(*.txt)", "PDF文件(*.pdf)", "Word文件(*.docx)"])
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            if file_path.endswith('.txt'):
                return TextDocument(file_path)
            elif file_path.endswith('.docx'):
                return DocDocument(file_path)
            elif file_path.endswith('.pdf'):
                return PdfDocument(file_path)
            else:
                QMessageBox.critical(None, "错误", "不支持的文件格式")
        return None
