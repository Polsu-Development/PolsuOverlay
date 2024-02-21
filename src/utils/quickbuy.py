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
┃                               © 2023 - 2024, Polsu Development - All rights reserved                                 ┃
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
from ..PolsuAPI import Player

from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap


import asyncio
import traceback


def displayQuickbuy(win, player: Player) -> None:
        """
        Display the quickbuy window
        
        :param win: The main window
        :param player: The player
        """
        if win.quickbuyWindow is not None:
            win.quickbuyWindow.close()

        win.quickbuyWindow = QuickbuyWindow(win, player, win.table.quickbuy)
        win.quickbuyWindow.run()


class QuickbuyImage():
    """
    A class representing a Hypixel Bedwars quickbuy image
    """
    def __init__(self, win) -> None:
        """
        Initialise the QuickbuyImage class
        
        :param win: The main window
        """
        self.win = win

        self.threads = {}
        self.cache = {}

        self.loading = []


    def run(self, player) -> None:
        """
        Run the QuickbuyImage class
        
        :param player: The player to get the quickbuy image
        """
        if player.username in self.loading:
            return
        else:
            if player.username in self.cache:
                self.setPixmap(player, self.cache[player.username], False)
            else:
                try:
                    self.threads[player.username] = Worker(self.win.player.client, player)
                    self.threads[player.username].update.connect(self.setPixmap)
                    self.threads[player.username].start()

                    self.loading.append(player.username)
                except:
                    self.win.logger.error(f"An error occurred while loading the quickbuy image!\n\nTraceback: {traceback.format_exc()}")


    def setPixmap(self, player, pixmap: QPixmap, cache: bool = True)  -> None:
        """
        Callback function to set the pixmap of the quickbuy image
        
        :param player: The player
        :param pixmap: The pixmap to set
        :param cache: Whether to cache the pixmap or not
        """
        if not pixmap.isNull():
            if cache:
                self.cache[player.username] = pixmap
                self.loading.remove(player.username)

            pixmap = pixmap.scaledToHeight(1000).scaledToWidth(800)

            if not self.win.quickbuyWindow:
                self.win.quickbuyWindow = QuickbuyWindow(self.win, player, self)
                self.win.quickbuyWindow.run()

            self.win.quickbuyWindow.label.setPixmap(pixmap)
            self.win.quickbuyWindow.label.setGeometry(0, 0, pixmap.size().width(), pixmap.size().height())

            self.win.quickbuyWindow.resize(pixmap.size().width(), pixmap.size().height())
            self.win.quickbuyWindow.setFixedSize(pixmap.size().width(), pixmap.size().height())
            self.win.quickbuyWindow.show()
        else:
            self.win.notif.send(
                title="Error...",
                message="Something went wrong while loading the quickbuy image!"
            )


class Worker(QThread):
    """
    A QThread that will request the API to load the quickbuy image
    """
    update = pyqtSignal(object, object)

    def __init__(self, client, player: Player) -> None:
        """
        Initialise the Worker class
        
        :param client: The client to request the API
        :param player: The player to get the quickbuy image
        """
        super(QThread, self).__init__()
        self.client = client
        self.player = player


    def run(self) -> None:
        """
        Run the Worker class
        """
        try:
            data = asyncio.run(self.client.player.loadQuickbuy(self.player.uuid))

            pixmap = QPixmap()
            pixmap.loadFromData(data)
        except:
            pixmap = QPixmap()

        self.update.emit(self.player, pixmap)


class QuickbuyWindow(QMainWindow):
    """
    Quickbuy window
    """
    def __init__(self, window, player: Player, quickbuy: QuickbuyImage) -> None:
        """
        Initialise the QuickbuyWindow class
        
        :param window: The main window
        :param player: The player to get the quickbuy image
        :param quickbuy: The quickbuy image
        """
        super().__init__()
        self.win = window
        self.player = player
        self.quickbuy = quickbuy

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.setWindowTitle(f"Quickbuy of {player.username}")
        self.setWindowIcon(QIcon(f"{self.win.pathAssets}/game-icons/Hypixel.png"))

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setStyleSheet("background: #36393F")
        self.setWindowOpacity(100)

        self.label = QLabel(self)
    

    def run(self) -> None:
        """
        Run the QuickbuyWindow
        """
        self.quickbuy.run(self.player)


    def closeEvent(self, event) -> None:
        """
        Close the QuickbuyWindow
        """
        self.win.quickbuyWindow = None
        event.accept()
