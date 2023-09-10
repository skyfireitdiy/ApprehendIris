from YiYan.YiYanConfigUI import Ui_YiYanConfig
from PyQt6.QtWidgets import QDialog

class YiYanConfig(QDialog):
    def __init__(self, parent=None):
        super(YiYanConfig, self).__init__(parent)

        self.ui = Ui_YiYanConfig()
        self.ui.setupUi(self)

    def accept(self)->None:
        if not self.ui.ledt_appid.text() or not self.ui.ledt_api_secret.text():
            QMessageBox.critical(self, "错误", "请将信息填写完整")
            return
        return super().accept()

    def GetConfig(self)->dict:
        return {
                "api_key": self.ui.ledt_appid.text(),
                "api_secret": self.ui.ledt_api_secret.text()
                }
