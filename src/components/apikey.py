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
from src import __version__
from ..utils.text import text2html
from ..utils.apikey import loadUpdate
from ..utils.menu import menuPaintEvent, leftMenuPaintEvent


from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QSize
from PyQt5.QtGui import QIcon


from datetime import datetime

import webbrowser


def openSettings(window) -> None:
    """
    Open the settings menu

    :param window: The Overlay window
    """
    window.logger.info(f"No API Key found, opening the API Key menu...")

    window.searchBox.setEnabled(False)
    window.searchIcon.setEnabled(False)

    window.apikeymenu = APIKeyMenu(window)
    window.apikeymenu.move(0, 34)
    window.apikeymenu.resize(window.width(), window.height())
    window.apikeymenu.SIGNALS.CLOSE.connect(window.close_apikey_menu)
    window.apikeymenu.show()

    window._apiKeyMenuOpened = True


class WidgetSignals(QObject):
    """
    WidgetSignals is a class that contains signals for the APIKeyMenu
    """
    CLOSE = pyqtSignal()


class APIKeyMenu(QWidget):
    """
    APIKeyMenu is a QWidget that contains the API Key menu
    """
    def __init__(self, window) -> None:
        """
        Initialise the APIKeyMenu

        :param window: The Overlay window
        """
        super(APIKeyMenu, self).__init__(window)
        self.win = window

        self.sentNotification = False

        text = QLabel("API", self)
        text.setFont(self.win.getFont())
        text.adjustSize()
        text.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
        text.setGeometry(20, 11, 190, 40)

        text = QLabel("Github", self)
        text.setFont(self.win.getFont())
        text.adjustSize()
        text.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
        text.setGeometry(20, 56, 190, 40)

        text = QLabel("Website", self)
        text.setFont(self.win.getFont())
        text.adjustSize()
        text.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
        text.setGeometry(20, 101, 190, 40)

        text = QLabel("Discord", self)
        text.setFont(self.win.getFont())
        text.adjustSize()
        text.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
        text.setGeometry(20, 146, 190, 40)


        self.apiButton = QPushButton(self)
        self.apiButton.setIcon(QIcon(self.win.getIconPath("api")))
        self.apiButton.setToolTip('https://api.polsu.xyz')
        self.apiButton.setIconSize(QSize(24, 24))
        self.apiButton.clicked.connect(lambda: webbrowser.open('https://api.polsu.xyz'))

        self.githubButton = QPushButton(self)
        self.githubButton.setIcon(QIcon(self.win.getIconPath("github")))
        self.githubButton.setToolTip('https://github.com/Polsu-Development')
        self.githubButton.setIconSize(QSize(24, 24))
        self.githubButton.clicked.connect(lambda: webbrowser.open('https://github.com/Polsu-Development'))

        self.websiteButton = QPushButton(self)
        self.websiteButton.setIcon(QIcon(self.win.getIconPath("website")))
        self.websiteButton.setToolTip('https://polsu.xyz')
        self.websiteButton.setIconSize(QSize(24, 24))
        self.websiteButton.clicked.connect(lambda: webbrowser.open('https://polsu.xyz'))

        self.discordButton = QPushButton(self)
        self.discordButton.setIcon(QIcon(self.win.getIconPath("discord")))
        self.discordButton.setToolTip('https://discord.polsu.xyz')
        self.discordButton.setIconSize(QSize(24, 24))
        self.discordButton.clicked.connect(lambda: webbrowser.open('https://discord.polsu.xyz'))


        self.apiButton.setGeometry(15, 12, 190, 40)
        self.githubButton.setGeometry(15, 57, 190, 40)
        self.websiteButton.setGeometry(15, 102, 190, 40)
        self.discordButton.setGeometry(15, 147, 190, 40)


        self.apiButton.setStyleSheet(self.win.themeStyle.sideBarButtonsStyle)
        self.githubButton.setStyleSheet(self.win.themeStyle.sideBarButtonsStyle)
        self.websiteButton.setStyleSheet(self.win.themeStyle.sideBarButtonsStyle)
        self.discordButton.setStyleSheet(self.win.themeStyle.sideBarButtonsStyle)


        label = QLabel(text2html(f"§7Polsu Overlay v{__version__}", size=12, bold=True), self)
        label.setFont(self.win.getFont())
        label.move(14, self.win.size().height()-90)

        label = QLabel(text2html(f"§8© 2022 - {datetime.now().year} Polsu Development.", size=6, bold=True), self)
        label.setFont(self.win.getFont())
        label.move(20, self.win.size().height()-65)

        label = QLabel(text2html(f"§8All rights reserved.", size=6, bold=True), self)
        label.setFont(self.win.getFont())
        label.move(60, self.win.size().height()-55)

        self.win.setMinimumSize(714, 352)

        self.settingsMenu = Settings(self.win)
        self.settingsMenu.setGeometry(self.win.POPUPWIDTH, 34, self.win.width(), self.win.height())
        self.settingsMenu.show()

        self.SIGNALS = WidgetSignals()


    def paintEvent(self, event) -> None:
        """
        Draw the API Key menu
        
        :param event: The paint event
        """
        return leftMenuPaintEvent(self)


class Settings(QWidget):
    """
    Settings is a QWidget that contains the settings menu
    """
    def __init__(self, parent) -> None:
        """
        Initialise the Settings menu
        
        :param parent: The parent of the Settings menu
        """
        super(Settings, self).__init__(parent)
        self.win = parent

        self.threads = {}

        label = QLabel(text2html(f"§fAPI Key:", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(20, 17)

        self.apikeyBox = QLineEdit(self)
        self.apikeyBox.setFont(self.win.getFont())
        self.apikeyBox.setMaxLength(36)
        self.apikeyBox.setStyleSheet(self.win.themeStyle.settingsAPIKeyStyle)
        self.apikeyBox.setPlaceholderText("Enter your Polsu API Key")
        self.apikeyBox.setGeometry(110, 15, 280, 28)
        self.apikeyBox.textChanged.connect(lambda: loadUpdate(self))
        self.apikeyBox.setFocusPolicy(Qt.StrongFocus)

        self.apikeyBox.setPlaceholderText(f"{self.win.configAPIKey[0:4]}XXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")

        self.searchIcon = QPushButton(QIcon(f"{self.win.pathAssets}/polsu/Polsu_.png"), "", self)
        self.searchIcon.setIconSize(QSize(18, 18))
        self.searchIcon.clicked.connect(lambda: self.apikeyBox.setFocus())
        self.searchIcon.setStyleSheet("QPushButton {border: 0; background: transparent;} QPushButton::hover {border-radius: 4px;}")
        self.searchIcon.setGeometry(113, 18, 19, 19)

        text = QLabel(text2html(f"§fGet your Key", bold=True), self)
        text.setFont(self.win.getFont())
        text.adjustSize()
        text.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
        text.setGeometry(20, 60, 190, 40)

        self.apikey = QPushButton(self)
        self.apikey.setIcon(QIcon(self.win.getIconPath("website")))
        self.apikey.setToolTip('Get your API Key')
        self.apikey.setIconSize(QSize(24, 24))
        self.apikey.clicked.connect(self.openAndMinimize)

        self.apikey.setGeometry(20, 60, 190, 40)
        self.apikey.setStyleSheet(self.win.themeStyle.sideBarButtonsStyle)

        label = QLabel(text2html(f"§fNeed help? Join our discord server!", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(20, 250)

        self.SIGNALS = WidgetSignals()

    
    def openAndMinimize(self) -> None:
        """
        Open the website to get the API Key
        """
        webbrowser.open('https://polsu.xyz/api/apikey')
        self.win.showMinimized()


    def close_settings(self) -> None:
        """
        Close the settings menu
        """
        self.close()


    def paintEvent(self, event) -> None:
        """
        Draw the settings menu
        
        :param event: The paint event
        """
        return menuPaintEvent(self)


    def _onclose(self) -> None:
        """
        Emit the close signal
        """
        self.SIGNALS.CLOSE.emit()
