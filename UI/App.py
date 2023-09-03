from UI.AppUI import Ui_App
from PyQt6.QtWidgets import QFileDialog, QDialog, QMessageBox, QPushButton, QTableWidgetItem, QAbstractItemView, QApplication
from PyQt6.QtCore import QLocale
from TextDocument import TextDocument
from DocDocument import DocDocument
from PdfDocument import PdfDocument
from UrlDocument import UrlDocument
from PlainTextDocument import PlainTextDocument
from UI.LineInput import GetLineInput
from UI.PlainTextInput import GetPlainTextInput
from Spark.SparkLLM import Spark
from ApprehendIrisService import ApprehendIrisService
from NLPService import NLPService
import pickle

class App(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = Ui_App()
        self.ui.setupUi(self)

        self.data_source = []
        self.llm_config = {}

        self.text_data = ""

        self.ui.tbl_data_source.setColumnCount(4)
        self.ui.tbl_data_source.setHorizontalHeaderLabels(["ID" ,"数据源", "数据", "操作"])

        self.ui.btn_file.clicked.connect(self.ChooseFile)
        self.ui.btn_url.clicked.connect(self.AddUrl)
        self.ui.btn_plaintext.clicked.connect(self.AddPlainText)
        self.ui.btn_send.clicked.connect(self.Send)
        self.ui.btn_save.clicked.connect(self.Save)
        self.ui.btn_load.clicked.connect(self.Load)
        self.ui.plain_exttext.textChanged.connect(self.UpdateTextOnUi)

    def AddPlainText(self):
        text, result = GetPlainTextInput("输入", "请输入文本")
        if not result:
            return
        if not text:
            self.ShowErrorMessage("请输入文本")
            return
        self.data_source.append(PlainTextDocument(text))
        self.UpdateTextOnUi()

    def AddFile(self, file_path):
        if file_path.endswith('.txt'):
            self.data_source.append(TextDocument(file_path))
        elif file_path.endswith('.docx'):
            self.data_source.append(DocDocument(file_path))
        elif file_path.endswith('.pdf'):
            self.data_source.append(PdfDocument(file_path))
        else:
            self.ShowErrorMessage("不支持的文件格式")
        self.UpdateTextOnUi()

    def AddUrl(self):
        url, result = GetLineInput("输入", "URL", "请输入url")
        if not result:
            return
        if not url:
            self.ShowErrorMessage("请输入URL")
            return
        self.data_source.append(UrlDocument(url))
        self.UpdateTextOnUi()


    def RemoveDataSource(self, file_id):
        for document in self.data_source:
            if document.ID() == file_id:
                if not self.ShowConfirmationDialog(f"确认删除{file_id}？"):
                    return
                self.data_source.remove(document)
                self.UpdateTextOnUi()
                return
        self.ShowErrorMessage(f"未找到数据源{file_id}")

    def UpdateTextOnUi(self):
        self.text_data = ""

        self.ui.tbl_data_source.setRowCount(0)
        for document in self.data_source:
            self.ui.tbl_data_source.setRowCount(self.ui.tbl_data_source.rowCount() + 1)
            self.ui.tbl_data_source.setItem(self.ui.tbl_data_source.rowCount() - 1, 0, 
                QTableWidgetItem(document.ID()))
            self.ui.tbl_data_source.setItem(self.ui.tbl_data_source.rowCount() - 1, 1, 
                QTableWidgetItem(document.Name()))
            tmp_text = document.GetText()
            self.text_data += tmp_text + "\n"
            self.ui.tbl_data_source.setItem(self.ui.tbl_data_source.rowCount() - 1, 2, 
                                            QTableWidgetItem(tmp_text if len(tmp_text) < 16 else tmp_text[:16] + "..."))
            btn = QPushButton("删除")
            btn.clicked.connect(lambda: self.RemoveDataSource(document.ID()))
            self.ui.tbl_data_source.setCellWidget(self.ui.tbl_data_source.rowCount() - 1, 3, 
                btn)

        self.text_data += self.ui.plain_exttext.toPlainText()

    def ChooseFile(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilters(["文本文件(*.txt)", "PDF文件(*.pdf)", "Word文件(*.docx)"])
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()[0]
            self.AddFile(selected_files)

    def ShowConfirmationDialog(self, tip)->bool:
        return QMessageBox.question(self, "确认", tip , QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes

    def ShowErrorMessage(self, message):
        QMessageBox.critical(self, "错误",message) 

    def ShowInfoMessage(self, message):
        QMessageBox.information(self, "信息", message) 

    def CheckValid(self)->bool:
        if self.ui.plain_input.toPlainText() == "":
            self.ShowErrorMessage("没有输入问题")
            return False
        if self.text_data == "":
            self.ShowErrorMessage("没有数据源")
            return False
        if self.ui.radio_spark.isChecked() and self.ui.ledt_api_secret.text() == "" or self.ui.ledt_api_key.text() == "" or self.ui.ledt_appid.text() == "":
            self.ShowErrorMessage("没有输入Spark认证信息")
            return False

        return True

    def GetSparkConfig(self)->dict:
        return {
            "api_secret": self.ui.ledt_api_secret.text(),
            "api_key": self.ui.ledt_api_key.text(),
            "appid": self.ui.ledt_appid.text()
        }

    def RestoreSparkConfig(self, data):
        self.ui.ledt_api_secret.setText(data["api_secret"])
        self.ui.ledt_api_key.setText(data["api_key"])
        self.ui.ledt_appid.setText(data["appid"])


    def Save(self):
        if 'Spark' not in self.llm_config.keys():
            self.llm_config['Spark'] = self.GetSparkConfig()
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            with open(selected_file, "wb") as fp:
                pickle.dump(self.llm_config, fp)

    def Load(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            with open(selected_file, "rb") as fp:
                self.llm_config = pickle.load(fp)
                if 'Spark' in self.llm_config.keys():
                    data = self.llm_config['Spark']
                    self.RestoreSparkConfig(data)
            
    def MakeKeySentenceInfo(self, sts)->str:
        ret = ""
        for i,s in enumerate(sts):
            ret += f"序号{i}. 相关度：{s[0]} 位置：({s[2][0]},{s[2][1]})\n{s[1]}\n"
        return ret

    def Send(self):
        if not self.CheckValid():
            return
        if self.ui.radio_spark.isChecked():
            llm = Spark(self.ui.ledt_appid.text(), self.ui.ledt_api_secret.text(), self.ui.ledt_api_key.text())
        else:
            self.ShowErrorMessage("没有合适的LLM")
            return
        #  nlp_service = NLPService(0, 5, 10, 'BERT', False)
        nlp_service = NLPService()
        question = self.ui.plain_input.toPlainText()
        sts = nlp_service.GetKeySentences(self.text_data, question)
        self.ui.plain_preview.setPlainText(self.MakeKeySentenceInfo(sts))
        self.ui.plain_input.clear()
        self.ui.palin_result.appendPlainText("问题：" + question + "\n")
        answer = ApprehendIrisService.Ask(llm, sts, question)
        self.ui.palin_result.appendPlainText("AI:\n" + answer + "\n")


