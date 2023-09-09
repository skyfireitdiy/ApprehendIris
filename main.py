from UI.App import App
from PyQt6 import QtWidgets
from UI.StyleSheet import qss
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qss)
    ui = App()
    ui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
