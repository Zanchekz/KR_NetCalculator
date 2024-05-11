import sys


from PyQt5.QtWidgets import QApplication

from ui import calcNetUi

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = calcNetUi()
    ui.show()

    sys.exit(app.exec())