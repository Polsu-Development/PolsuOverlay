from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWinExtras import QtWin


import requests


class QuickbuyImage():
    """
    A class representing a Hypixel Bedwars quickbuy image
    """
    def __init__(self, win) -> None:
        self.win = win

        self.threads = {}


    def run(self, url):
        self.threads[url] = Worker(url)
        self.threads[url].update.connect(self.setPixmap)
        self.threads[url].start()


    def setPixmap(self, pixmap: QPixmap):
        if not pixmap.isNull():
            pixmap = pixmap.scaledToHeight(1000).scaledToWidth(800)
            self.win.quickbuyWindow.label.setPixmap(pixmap)
            self.win.quickbuyWindow.label.setGeometry(0, 0, pixmap.size().width(), pixmap.size().height())

            self.win.quickbuyWindow.resize(pixmap.size().width(), pixmap.size().height())
            self.win.quickbuyWindow.setFixedSize(pixmap.size().width(), pixmap.size().height())
            self.win.quickbuyWindow.show()
        else:
            self.win.notif.send(
                title="Error - Quickbuy not loaded!",
                message="This quickbuy is loading, please try again in a few seconds..."
            )


class Worker(QThread):
    update = pyqtSignal(object)

    def __init__(self, url):
        super(QThread, self).__init__()
        self.url = url


    def run(self):
        try:
            response = requests.get(self.url)
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
        except:
            pixmap = QPixmap()

        self.update.emit(pixmap)


class QuickbuyWindow(QMainWindow):
    def __init__(self, window, username, quickbuy: QuickbuyImage, url):
        super().__init__()
        self.win = window

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        QtWin.enableBlurBehindWindow(self)

        self.setWindowTitle(f"Quickbuy of {username}")
        self.setWindowIcon(QIcon(f"{self.win.pathAssets}/game-icons/Hypixel.png"))

        self.setStyleSheet("background: transparent")
        

        self.label = QLabel(self)
        quickbuy.run(url)


    def closeEvent(self, event):
        self.win.quickbuyWindow = None
        event.accept()
