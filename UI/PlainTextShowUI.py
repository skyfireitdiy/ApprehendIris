# Form implementation generated from reading ui file 'UI\PlainTextShow.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PlainTextShow(object):
    def setupUi(self, PlainTextShow):
        PlainTextShow.setObjectName("PlainTextShow")
        PlainTextShow.resize(938, 598)
        self.verticalLayout = QtWidgets.QVBoxLayout(PlainTextShow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plain_content = QtWidgets.QPlainTextEdit(parent=PlainTextShow)
        self.plain_content.setReadOnly(True)
        self.plain_content.setObjectName("plain_content")
        self.verticalLayout.addWidget(self.plain_content)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=PlainTextShow)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PlainTextShow)
        self.buttonBox.accepted.connect(PlainTextShow.accept) # type: ignore
        self.buttonBox.rejected.connect(PlainTextShow.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(PlainTextShow)

    def retranslateUi(self, PlainTextShow):
        _translate = QtCore.QCoreApplication.translate
        PlainTextShow.setWindowTitle(_translate("PlainTextShow", "Dialog"))
