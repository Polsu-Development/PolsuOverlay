"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                      ┃
┃                                                  Polsu's Overlay                                                     ┃
┃                                                                                                                      ┃
┃                                                                                                                      ┃
┃  • A Hypixel Bedwars Overlay in Python, 100% free and open source!                                                   ┃
┃  > https://github.com/Polsu-Development/PolsuOverlay                                                                 ┃
┃  • Made by Polsu's Development Team                                                                                  ┃
┃                                                                                                                      ┃
┃                                                                                                                      ┃
┃                                                                                                                      ┃
┃                                   © 2023, Polsu Development - All rights reserved                                    ┃
┃                                                                                                                      ┃
┃  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the    ┃
┃  following conditions are met:                                                                                       ┃
┃                                                                                                                      ┃
┃  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the           ┃
┃     following disclaimer.                                                                                            ┃
┃                                                                                                                      ┃
┃  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the        ┃
┃     following disclaimer in the documentation and/or other materials provided with the distribution.                 ┃
┃                                                                                                                      ┃
┃  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,  ┃
┃  INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE   ┃
┃  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,  ┃
┃  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR     ┃
┃  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,   ┃
┃  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE    ┃
┃  USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                                            ┃
┃                                                                                                                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
from ..PolsuAPI import Polsu, Player
from ..utils.quickbuy import displayQuickbuy
from .sorting import TableSortingItem


from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QColor


import asyncio


class SkinIcon():
    """
    A class representing a Minecraft skin icon
    """
    def __init__(self, win, table) -> None:
        """
        Initialise the SkinIcon class
        
        :param win: The window
        :param table: The table
        :param client: The client
        """
        self.win = win
        self.table = table

        self.threads = {}
        self.cache = {}

        self.default = QIcon(f"{self.win.pathAssets}/steve.png")


    def loadSkin(self, player: Player, count: int) -> None:
        """
        Load the skin of the player
        
        :param player: The player to load the skin
        :param count: The position of the player in the table
        """
        if player.username in self.cache:
            self.setSkin(self.cache[player.username], player, count)
        else:
            button = QPushButton(self.table)
            button.setIcon(self.default)
            if not player.nicked:
                button.setStyleSheet(self.win.themeStyle.buttonsStyle)
                button.clicked.connect(lambda: displayQuickbuy(self.win, player))
            button.setProperty("name", "head")

            for row in range(self.table.rowCount()):
                _item = self.table.item(row, 2)

                if _item and _item.value == player.username:
                    self.table.setCellWidget(row, 0, button)
                    self.table.setItem(row, 0, TableSortingItem(count))

            self.threads[player.username] = Worker(player, self.win.player.client, self.default, count)
            self.threads[player.username].update.connect(self.setSkin)
            self.threads[player.username].start()


    def setSkin(self, icon: QIcon, player: Player, count: int, cache: bool = True) -> None:
        """
        Callback function to set the skin of the player
        
        :param icon: The icon to set
        :param player: The player
        :param count: The position of the player in the table
        :param cache: Whether to cache the skin or not
        """
        if cache:
            self.cache[player.username] = icon

        button = QPushButton(self.table)
        button.setIcon(icon)
        if not player.nicked:
            button.setStyleSheet(self.win.themeStyle.buttonsStyle)
            button.clicked.connect(lambda: displayQuickbuy(self.win, player))
        button.setProperty("name", "head")

        for row in range(self.table.rowCount()):
            _item = self.table.item(row, 2)

            if _item and _item.value == player.username:
                self.table.setCellWidget(row, 0, button)
                self.table.setItem(row, 0, TableSortingItem(count))

                if player.blacklisted.status or player.local.status:
                    color = QColor("#FF0000")
                    color.setAlpha(50)
                    
                    item = self.table.item(row, 0)
                    item.setBackground(color)


class Worker(QThread):
    """
    A QThread that will load the skin
    """
    update = pyqtSignal(object, object, int)

    def __init__(self, player, client: Polsu, default: QIcon, count: int) -> None:
        """
        Initialise the Worker class
        
        :param player: The player to load the skin
        :param client: The client to request the API
        :param default: The default icon
        """
        super(QThread, self).__init__()
        self.player = player
        self.client = client
        self.default = default
        self.count = count

        self.icon = QIcon()


    def run(self) -> None:
        """
        Run the Worker class
        """
        try:
            if self.player.uuid:
                data = asyncio.run(self.client.player.loadSkin(self.player))

                pixmap = QPixmap()
                pixmap.loadFromData(data)

                icon = QIcon(pixmap)
            else:
                raise Exception("No player found.")
        except:
            icon = self.default

        self.icon = icon
        self.update.emit(icon, self.player, self.count)
