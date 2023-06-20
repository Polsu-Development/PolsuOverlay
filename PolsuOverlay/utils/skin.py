from .sorting import TableSortingItem


from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap


import requests


class SkinIcon():
    def __init__(self, table):
        self.table = table

        self.threads = {}


    def loadSkin(self, player):
        self.threads[player.username] = Worker(player)
        self.threads[player.username].update.connect(self.setSkin)
        self.threads[player.username].start()

    
    def setSkin(self, icon, player):
        button = QPushButton(self.table)
        button.setIcon(icon)
        button.setProperty("name", "head")

        for row in range(self.table.rowCount()):
            _item = self.table.item(row, 2)

            if _item and _item.value == player.username:
                self.table.setCellWidget(row, 0, button)
                self.table.setItem(row, 0, TableSortingItem(player.bedwars.requeue.index))


class Worker(QThread):
    update = pyqtSignal(object, object)

    def __init__(self, player):
        super(QThread, self).__init__()
        self.player = player


    def run(self):
        try:
            if self.player.uuid:
                url = f"https://crafatar.com/avatars/{self.player.uuid}"
            else:
                url = "https://crafatar.com/avatars/c06f89064c8a49119c29ea1dbd1aab82"

            response = requests.get(url)
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            icon = QIcon(pixmap)
        except:
            icon = QIcon()

        self.update.emit(icon, self.player)
