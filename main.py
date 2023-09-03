from UI.App import App
from PyQt6 import QtWidgets
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = App()
    ui.show()
    sys.exit(app.exec())    


if __name__ == '__main__':
    main()
