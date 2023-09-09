from PyQt6.QtWidgets import QDialog
from UI.ChoiceUI import Ui_Choice


class Choice(QDialog):
    def __init__(self, title:str, tip:str, choice:[str],parent=None):
        super(Choice, self).__init__(parent)
        self.ui = Ui_Choice()
        self.ui.setupUi(self)

        self.setWindowTitle(title)
        self.ui.lab_tip.setText(tip)
        self.ui.com_choice.addItems(choice)

    def GetChoice(self)->str:
        return self.ui.com_choice.currentText()


def GetChoice(title:str, tip:str, choice:[str])->str:
    dlg = Choice(title, tip, choice)
    if dlg.exec():
        return dlg.GetChoice()
    return None

