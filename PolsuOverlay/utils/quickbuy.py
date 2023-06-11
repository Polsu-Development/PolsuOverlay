from PyQt5.QtGui import QPixmap


import requests


class QuickbuyImage:
    """
    A class representing a Hypixel Bedwars quickbuy image
    """
    def __init__(self, url: str) -> None:
        self.url = url

        try:
            response = requests.get(self.url)
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(response.content)
        except:
            self.pixmap = QPixmap()
