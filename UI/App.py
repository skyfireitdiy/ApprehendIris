from UI.AppUI import Ui_App
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QPushButton, QTableWidgetItem, QHBoxLayout, QWidget, QRadioButton
from PyQt6.QtCore import pyqtSignal
from TFIDFService import TFIDFService
from Spark.SparkUI import SpackUI
from UI.PlainTextShow import PlainTextShow
from FileDataSource.FileDataSource import FileDataSource
from UrlDataSource.UrlDataSource import UrlDataSource
from PlainTextDataSource.PlainTextDataSource import PlainTextDataSource
from BrowserDataSource.BrowserDataSource import BrowserDataSource
import json
import threading


class App(QMainWindow):

    log_message_sent = pyqtSignal(str)
    progress_sent = pyqtSignal(int)
    output_sent = pyqtSignal(str)
    result_sent = pyqtSignal(str)
    extdata_sent = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.ui = Ui_App()
        self.ui.setupUi(self)

        self.ui.tbl_data_source.setColumnCount(4)
        self.ui.tbl_data_source.setHorizontalHeaderLabels(
                ["ID", "数据源", "数据", "操作"])

        self.ui.btn_send.clicked.connect(self.Send)
        self.ui.btn_save_config.clicked.connect(self.Save)
        self.ui.btn_load_config.clicked.connect(self.Load)
        self.ui.plain_exttext.textChanged.connect(self.UpdateTextOnUi)
        self.ui.btn_model_config.clicked.connect(self.ModelConfig)
        self.ui.btn_del_node.clicked.connect(self.DeleteLastNode)
        self.ui.btn_choose_model.clicked.connect(self.ChooseModel)
        self.ui.check_to_exttext.clicked.connect(self.SetAppendResultToExt)
        self.ui.btn_clear_log.clicked.connect(self.ui.plain_log.clear)
        self.ui.btn_add_document.clicked.connect(self.AddDocument)

        self.progress_sent.connect(self.ui.progress_bar.setValue)
        self.log_message_sent.connect(self.ui.plain_log.append)
        self.output_sent.connect(self.ui.plain_result.append)
        self.extdata_sent.connect(self.ui.plain_exttext.appendPlainText)
        self.result_sent.connect(self.HandleResult)

        self.documents = []
        self.models = {}
        self.models_check = {}
        self.config = {
                "Models": {},
                "Chain": [],
                "AppendResultToExt": True
                }

        self.data_sources = {}
        self.data_sources_check = {}

        self.current_model = ""
        self.current_data_source = ""
        self.text_data = ""

        self.AddModel("Spark", SpackUI())

        tfidf_service = TFIDFService()
        tfidf_service.SetLogger(self.log_message_sent.emit)
        tfidf_service.SetProgressCallback(self.progress_sent.emit)
        self.AddModel("TF-IDF", tfidf_service)


        self.AddDataSource("文件", FileDataSource())
        self.AddDataSource("URL", UrlDataSource())
        self.AddDataSource("纯文本", PlainTextDataSource())
        self.AddDataSource("浏览器", BrowserDataSource())

        self.UpdateModelToUI()

    def HandleResult(self, result):
        self.ui.btn_send.setEnabled(True)

    def SetAppendResultToExt(self, x):
        self.config["AppendResultToExt"] = x

    def ChooseModel(self):
        if self.current_model == "":
            self.ShowErrorMessage("未选择模型")
            return
        if not self.models[self.current_model].Configed():
            self.ShowErrorMessage("模型未配置")
            return
        self.config["Chain"].append(self.current_model)
        self.UpdateModelToUI()

    def DeleteLastNode(self):
        if len(self.config["Chain"]) > 0:
            self.config["Chain"].pop()
            self.UpdateModelToUI()

    def ModelConfig(self):
        if not self.current_model:
            self.ShowErrorMessage("未选择模型")
            return
        c = self.models[self.current_model].GetConfig()
        if c:
            self.config["Models"][self.current_model] = c
            self.SetConfigToModel()
            self.UpdateModelToUI()

    def AddDocument(self):
        if not self.current_data_source:
            self.ShowErrorMessage("未选择数据源")
            return
        c = self.data_sources[self.current_data_source].CreateDocument()
        if c:
            self.documents.append(c)
            self.UpdateTextOnUi()

    def SetConfigToModel(self):
        for name, cfg in self.config["Models"].items():
            if name in self.models:
                self.models[name].SetConfig(cfg)

    def AddDataSource(self, name, data_source):
        self.data_sources[name] = data_source
        check = QRadioButton(name)

        def set_current():
            nonlocal check
            nonlocal name
            if check.isChecked():
                self.current_data_source = name
        check.clicked.connect(set_current)
        self.data_sources_check[name] = check
        self.ui.layout_data_source.addWidget(check)
        self.UpdateModelToUI()

    def AddModel(self, name, llm):
        self.models[name] = llm
        check = QRadioButton(name)

        def set_current():
            nonlocal check
            nonlocal name
            if check.isChecked():
                self.current_model = name
        check.clicked.connect(set_current)
        self.models_check[name] = check
        self.ui.layout_models.addWidget(check)
        self.UpdateModelToUI()

    def UpdateModelToUI(self):
        for name, model in self.models.items():
            self.models_check[name].setText(
                    name+"("+model.Description()+")(已配置)" if model.Configed() else name+"("+model.Description()+")(未配置)")

        self.ui.lab_chain.setText('->'.join(self.config["Chain"]))
        self.ui.check_to_exttext.setChecked(self.config["AppendResultToExt"])

    def RemoveDocument(self, file_id):
        for document in self.documents:
            if document.ID() == file_id:
                if not self.ShowConfirmationDialog(f"确认删除{file_id}？"):
                    return
                self.documents.remove(document)
                self.UpdateTextOnUi()
                return
        self.ShowErrorMessage(f"未找到数据源{file_id}")

    def UpdateTextOnUi(self):
        self.text_data = ""

        self.ui.tbl_data_source.setRowCount(0)
        for document in self.documents:
            self.ui.tbl_data_source.setRowCount(
                    self.ui.tbl_data_source.rowCount() + 1)
            self.ui.tbl_data_source.setItem(self.ui.tbl_data_source.rowCount() - 1, 0,
                                            QTableWidgetItem(document.ID()))
            self.ui.tbl_data_source.setItem(self.ui.tbl_data_source.rowCount() - 1, 1,
                                            QTableWidgetItem(document.Name()))
            tmp_text = document.GetText()
            self.text_data += tmp_text + "\n"
            self.ui.tbl_data_source.setItem(self.ui.tbl_data_source.rowCount() - 1, 2,
                                            QTableWidgetItem(tmp_text if len(tmp_text) < 16 else tmp_text[:16] + "..."))

            wgt = QWidget()
            btn_refresh=QPushButton("刷新")
            btn_show = QPushButton("查看")
            btn_remove = QPushButton("删除")

            def Refresh(d):
                def inner():
                    d.ForceGetText()
                return inner

            def ShowContent(content):
                def inner():
                    PlainTextShow(content).exec()
                return inner

            def RemoveItem(self, id):
                def inner():
                    self.RemoveDocument(id)
                return inner

            btn_refresh.clicked.connect(Refresh(document))
            btn_show.clicked.connect(ShowContent(tmp_text))
            btn_remove.clicked.connect(RemoveItem(self, document.ID()))
            layout = QHBoxLayout()
            layout.addWidget(btn_refresh)
            layout.addWidget(btn_show)
            layout.addWidget(btn_remove)
            wgt.setLayout(layout)
            self.ui.tbl_data_source.setCellWidget(self.ui.tbl_data_source.rowCount() - 1, 3,
                                                  wgt)
        self.ui.tbl_data_source.resizeRowsToContents()

        self.text_data += self.ui.plain_exttext.toPlainText()

    def ChooseFile(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilters(
                ["文本文件(*.txt)", "PDF文件(*.pdf)", "Word文件(*.docx)"])
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()[0]
            self.AddFile(selected_files)

    def ShowConfirmationDialog(self, tip) -> bool:
        return QMessageBox.question(self, "确认", tip, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes

    def ShowErrorMessage(self, message):
        QMessageBox.critical(self, "错误", message)

    def ShowInfoMessage(self, message):
        QMessageBox.information(self, "信息", message)

    def CheckValid(self) -> bool:
        if self.ui.plain_input.toPlainText() == "":
            self.ShowErrorMessage("没有输入问题")
            return False
        if len(self.config["Chain"]) == 0:
            self.ShowErrorMessage("没有选择模型")
            return False

        return True

    def Save(self):
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            with open(selected_file, "w") as fp:
                json.dump(self.config, fp, indent=4)
                self.ShowInfoMessage("保存成功")

    def Load(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            with open(selected_file, "r") as fp:
                self.config = json.load(fp)
                self.SetConfigToModel()
                self.UpdateModelToUI()
                self.ShowInfoMessage("加载成功")

    def Run(self, data):
        question = data[1]
        for name in self.config["Chain"]:
            data = self.models[name].Chat(data)
            if data is None:
                break
        self.output_sent.emit(
                name+":\n" + "\n".join(data)+"\n==================\n" if data is not None else "没有找到答案")
        if self.config["AppendResultToExt"]:
            self.extdata_sent.emit(question+"\n"+'\n'.join(data)+"\n" if data is not None else "没有找到答案")
        self.result_sent.emit(''.join(data) if data is not None else "没有找到答案")

    def Send(self):
        if not self.CheckValid():
            return
        self.ui.btn_send.setEnabled(False)
        data = [self.text_data, self.ui.plain_input.toPlainText()]
        self.ui.plain_result.clear()
        self.ui.plain_input.clear()
        threading.Thread(target=self.Run, args=[data], daemon=True).start()
