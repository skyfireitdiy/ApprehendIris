from PyQt6.QtWidgets import QDialog, QMessageBox
from Spark.SparkConfigUI import Ui_SparkConfig


class SparkConfig(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_SparkConfig()
        self.ui.setupUi(self)

    def accept(self) -> None:
        if self.ui.ledt_api_key.text() == "" or self.ui.ledt_api_secret.text() == "" or self.ui.ledt_appid.text() == "":
            QMessageBox.critical(self, "错误", "请将信息填写完整")
            return
        return super().accept()

    def GetConfig(self):
        return {
            "api_secret": self.ui.ledt_api_secret.text(),
            "api_key": self.ui.ledt_api_key.text(),
            "appid": self.ui.ledt_appid.text()
        }
