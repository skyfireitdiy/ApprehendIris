from PyQt6.QtWidgets import QDialog
from UI.PlainTextShowUI import Ui_PlainTextShow


class PlainTextShow(QDialog):
    def __init__(self, content, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_PlainTextShow()
        self.ui.setupUi(self)

        self.ui.plain_content.setPlainText(content)
