# Form implementation generated from reading ui file 'UI\SparkConfig.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SparkConfig(object):
    def setupUi(self, SparkConfig):
        SparkConfig.setObjectName("SparkConfig")
        SparkConfig.resize(400, 158)
        self.verticalLayout = QtWidgets.QVBoxLayout(SparkConfig)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(parent=SparkConfig)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.ledt_api_secret = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.ledt_api_secret.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ledt_api_secret.setObjectName("ledt_api_secret")
        self.gridLayout_2.addWidget(self.ledt_api_secret, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.ledt_appid = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.ledt_appid.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ledt_appid.setObjectName("ledt_appid")
        self.gridLayout_2.addWidget(self.ledt_appid, 0, 1, 1, 1)
        self.ledt_api_key = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.ledt_api_key.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ledt_api_key.setObjectName("ledt_api_key")
        self.gridLayout_2.addWidget(self.ledt_api_key, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=SparkConfig)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SparkConfig)
        self.buttonBox.accepted.connect(SparkConfig.accept) # type: ignore
        self.buttonBox.rejected.connect(SparkConfig.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SparkConfig)

    def retranslateUi(self, SparkConfig):
        _translate = QtCore.QCoreApplication.translate
        SparkConfig.setWindowTitle(_translate("SparkConfig", "大模型配置"))
        self.groupBox_3.setTitle(_translate("SparkConfig", "讯飞星火大模型"))
        self.label.setText(_translate("SparkConfig", "appid"))
        self.label_2.setText(_translate("SparkConfig", "api secret"))
        self.label_3.setText(_translate("SparkConfig", "api key"))
