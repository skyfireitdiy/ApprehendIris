from PyQt6.QtWidgets import QDialog
from UI.PlainTextInputUI import Ui_PlainTextInput

class PlainTextInput(QDialog):
    def __init__(self, title, place_holder="", parent=None):
        super(QDialog, self).__init__(parent=parent)
        self.ui = Ui_PlainTextInput()
        self.ui.setupUi(self)
        
        self.setWindowTitle(title)
        self.ui.plain_input.setPlaceholderText(place_holder)


def GetPlainTextInput(title, place_holder=""):
    wgt = PlainTextInput(title=title, place_holder=place_holder)
    if wgt.exec() == QDialog.DialogCode.Accepted:
        return wgt.ui.plain_input.toPlainText(), True
    return None, False
