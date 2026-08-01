import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from . import services
from .app import App


def run():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("RunesCrypt")
    app.setStyle("Fusion")
    win = App(services)
    win.setWindowIcon(QIcon("img/icon.png"))
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
