from PyQt6.QtWidgets import QDialog
from UI.LineInputUI import Ui_LineInput


class LineEdit(QDialog):
    def __init__(self, title, tip, place_holder = "",parent=None):
        super(QDialog, self).__init__(parent=parent)
        self.ui = Ui_LineInput()
        self.ui.setupUi(self)

        self.setWindowTitle(title)
        self.ui.lab_tip.setText(tip)
        self.ui.ledt_input.setPlaceholderText(place_holder)



def GetLineInput(title, tip, place_holder=""):
    wgt = LineEdit(title, tip, place_holder)
    if wgt.exec() == QDialog.DialogCode.Accepted:
        return wgt.ui.ledt_input.text(), True
    return None, False
