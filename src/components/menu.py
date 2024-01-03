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
from .components import updateComponents
from .rpc import startRPC
from ..utils.text import text2html
from ..utils.apikey import loadUpdate
from ..utils.menu import menuPaintEvent, leftMenuPaintEvent


from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QLineEdit, QCheckBox, QSlider, QFileDialog, QDesktopWidget
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QSize
from PyQt5.QtGui import QIcon


from datetime import datetime
from getpass import getuser

import webbrowser


class WidgetSignals(QObject):
    """
    Widget Signals
    """
    CLOSE = pyqtSignal()


class Menu(QWidget):
    """
    Menu Widget
    """
    def __init__(self, win) -> None:
        """
        Initialise the Menu Widget
        
        :param win: The Overlay window
        """
        super(Menu, self).__init__(win)
        self.win = win


        # Background Button to close the Popup Menu
        self.close_menu = QPushButton("", self)
        self.close_menu.setGeometry(self.win.POPUPWIDTH, 2, self.win.width(), self.win.height())
        self.close_menu.setStyleSheet("QPushButton {border: 0; background: transparent;}")
        self.close_menu.clicked.connect(self._onclose)


        if self.win.height() >= 380:
            text = QLabel("Reload", self)
            text.setFont(self.win.getFont())
            text.adjustSize()
            text.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
            text.setGeometry(20, 11, 190, 40)

            text = QLabel("Settings", self)
            text.setFont(self.win.getFont())
            text.adjustSize()
            text.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
            text.setGeometry(20, 56, 190, 40)
            
            text = QLabel("About", self)
            text.setFont(self.win.getFont())
            text.adjustSize()
            text.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
            text.setGeometry(20, 101, 190, 40)

            text = QLabel("Github", self)
            text.setFont(self.win.getFont())
            text.adjustSize()
            text.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
            text.setGeometry(20, 146, 190, 40)

            text = QLabel("Website", self)
            text.setFont(self.win.getFont())
            text.adjustSize()
            text.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
            text.setGeometry(20, 191, 190, 40)

            text = QLabel("Discord", self)
            text.setFont(self.win.getFont())
            text.adjustSize()
            text.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
            text.setGeometry(20, 236, 190, 40)


        self.reloadButton = QPushButton(self)
        self.reloadButton.setIcon(QIcon(self.win.getIconPath("reload")))
        self.reloadButton.setToolTip('Reload the overlay')
        self.reloadButton.setIconSize(QSize(24, 24))
        self.reloadButton.clicked.connect(self.reload)
        
        self.settingsButton = QPushButton(self)
        self.settingsButton.setIcon(QIcon(self.win.getIconPath("settings")))
        self.settingsButton.setToolTip('Settings')
        self.settingsButton.setIconSize(QSize(24, 24))
        self.settingsButton.clicked.connect(self.openSettings)

        self.infoButton = QPushButton(self)
        self.infoButton.setIcon(QIcon(self.win.getIconPath("info")))
        self.infoButton.setToolTip('Help & Information')
        self.infoButton.setIconSize(QSize(24, 24))
        self.infoButton.clicked.connect(self.openInfo)

        self.websiteButton = QPushButton(self)
        self.websiteButton.setIcon(QIcon(self.win.getIconPath("github")))
        self.websiteButton.setToolTip('https://github.com/Polsu-Development')
        self.websiteButton.setIconSize(QSize(24, 24))
        self.websiteButton.clicked.connect(lambda: webbrowser.open('https://github.com/Polsu-Development'))

        self.apiButton = QPushButton(self)
        self.apiButton.setIcon(QIcon(self.win.getIconPath("website")))
        self.apiButton.setToolTip('https://polsu.xyz')
        self.apiButton.setIconSize(QSize(24, 24))
        self.apiButton.clicked.connect(lambda: webbrowser.open('https://polsu.xyz'))

        self.discordButton = QPushButton(self)
        self.discordButton.setIcon(QIcon(self.win.getIconPath("discord")))
        self.discordButton.setToolTip('https://discord.polsu.xyz')
        self.discordButton.setIconSize(QSize(24, 24))
        self.discordButton.clicked.connect(lambda: webbrowser.open('https://discord.polsu.xyz'))


        if self.win.height() >= 380:
            self.reloadButton.setGeometry(15, 12, 190, 40)
            self.settingsButton.setGeometry(15, 57, 190, 40)
            self.infoButton.setGeometry(15, 102, 190, 40)
            self.websiteButton.setGeometry(15, 147, 190, 40)
            self.apiButton.setGeometry(15, 192, 190, 40)
            self.discordButton.setGeometry(15, 237, 190, 40)


            self.reloadButton.setStyleSheet(self.win.themeStyle.sideBarButtonsStyle)
            self.settingsButton.setStyleSheet(self.win.themeStyle.sideBarButtonsStyle)
            self.infoButton.setStyleSheet(self.win.themeStyle.sideBarButtonsStyle)
            self.websiteButton.setStyleSheet(self.win.themeStyle.sideBarButtonsStyle)
            self.apiButton.setStyleSheet(self.win.themeStyle.sideBarButtonsStyle)
            self.discordButton.setStyleSheet(self.win.themeStyle.sideBarButtonsStyle)
        else:
            self.reloadButton.setGeometry(5, 12, 35, 35)
            self.settingsButton.setGeometry(45, 12, 35, 35)
            self.infoButton.setGeometry(85, 12, 35, 35)
            self.websiteButton.setGeometry(125, 12, 35, 35)
            self.apiButton.setGeometry(165, 12, 35, 35)
            self.discordButton.setGeometry(205, 12, 35, 35)

            
            self.reloadButton.setStyleSheet(self.win.themeStyle.sideBarSmallButtonsStyle)
            self.settingsButton.setStyleSheet(self.win.themeStyle.sideBarSmallButtonsStyle)
            self.infoButton.setStyleSheet(self.win.themeStyle.sideBarSmallButtonsStyle)
            self.websiteButton.setStyleSheet(self.win.themeStyle.sideBarSmallButtonsStyle)
            self.apiButton.setStyleSheet(self.win.themeStyle.sideBarSmallButtonsStyle)
            self.discordButton.setStyleSheet(self.win.themeStyle.sideBarSmallButtonsStyle)


        if self.win.width() > self.win.POPUPWIDTH+430 and self.win.height() > self.win.POPUPWIDTH+70:
            self.settingsButton.setEnabled(True)
            self.infoButton.setEnabled(True)
        else:
            self.settingsButton.setEnabled(False)
            self.infoButton.setEnabled(False)

        
        label = QLabel(text2html(f"§7Polsu Overlay v{__version__}", size=12, bold=True), self)
        label.setFont(self.win.getFont())
        label.move(14, self.win.size().height()-90)

        label = QLabel(text2html(f"§8© 2022 - {datetime.now().year} Polsu Development.", size=6, bold=True), self)
        label.setFont(self.win.getFont())
        label.move(20, self.win.size().height()-65)

        label = QLabel(text2html(f"§8All rights reserved.", size=6, bold=True), self)
        label.setFont(self.win.getFont())
        label.move(60, self.win.size().height()-55)

        self.SIGNALS = WidgetSignals()

        
    def reload(self) -> None:
        """
        Reload the overlay
        """
        #for player in self.win.player.threads:
        #    self.win.player.threads[player].terminate()
        
        #for player in self.win.table.skin.threads:
        #    self.win.table.skin.threads[player].terminate()

        self.win.table.resetTable()
        self.win.open_menu()

    
    def openInfo(self) -> None:
        """
        Open the Help & Information Popup Menu
        """
        if self.win._settingsMenuOpened:
            self.close_settingsMenu()
        if not self.win._infoMenuOpened:
            if self.win.width() > self.win.POPUPWIDTH+430 and self.win.height() > self.win.POPUPWIDTH+70:
                self.infoMenu = Info(self.win)
                self.infoMenu.setGeometry(self.win.POPUPWIDTH, 34, self.win.width(), self.win.height())
                self.infoMenu.SIGNALS.CLOSE.connect(self.close_infoMenu)
                self.win._infoMenuOpened = True
                self.infoMenu.show()
        else:
            self.close_infoMenu()


    def close_infoMenu(self, disable: bool = True) -> None:
        """
        Close the Help & Information Popup Menu
        
        :param disable: Disable the Popup Menu
        """
        self.infoMenu.close()
        if disable:
            self.win._infoMenuOpened = False
            

    def openSettings(self) -> None:
        """
        Open the Settings Popup Menu
        """
        if self.win._infoMenuOpened:
            self.close_infoMenu()
        if not self.win._settingsMenuOpened:
            if self.win.width() > self.win.POPUPWIDTH+430 and self.win.height() > self.win.POPUPWIDTH+70:
                self.settingsMenu = Settings(self.win)
                self.settingsMenu.setGeometry(self.win.POPUPWIDTH, 34, self.win.width(), self.win.height())
                self.settingsMenu.SIGNALS.CLOSE.connect(self.close_settingsMenu)
                self.win._settingsMenuOpened = True
                self.settingsMenu.show()
        else:
            self.close_settingsMenu()


    def close_settingsMenu(self, disable: bool = True) -> None:
        """
        Close the Settings Popup Menu
        
        :param disable: Disable the Popup Menu
        """
        self.settingsMenu.close_settings()
        if disable:
            self.win._settingsMenuOpened = False


    def paintEvent(self, event) -> None:
        """
        Paint the Menu Widget
        
        :param event: The event
        """
        return leftMenuPaintEvent(self)

    
    def _onclose(self) -> None:
        """
        Close the Menu Widget
        """
        self.SIGNALS.CLOSE.emit()


class Settings(QWidget):
    """
    Settings Widget
    """
    def __init__(self, win) -> None:
        """
        Initialise the Settings Widget
        
        :param win: The Overlay window
        """
        super(Settings, self).__init__(win)
        self.win = win
        
        self.win.loadThemes(self.win)

        self.threads = {}

        self.opacity = 0.8


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

        if self.win.configAPIKey != "":
            newString = ""
            for i in range(0, 4):
                newString += self.win.configAPIKey[i]
            
            newString += "XXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
            self.apikeyBox.setPlaceholderText(newString)


        self.searchIcon = QPushButton(QIcon(f"{self.win.pathAssets}/polsu/Polsu_.png"), "", self)
        self.searchIcon.setIconSize(QSize(18, 18))
        self.searchIcon.clicked.connect(lambda: self.apikeyBox.setFocus())
        self.searchIcon.setStyleSheet("QPushButton {border: 0; background: transparent;} QPushButton::hover {border-radius: 4px;}")
        self.searchIcon.setGeometry(113, 18, 19, 19)


        label = QLabel(text2html(f"§fTheme:", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(20, 50)

        self.themeMenu = QComboBox(self)
        self.themeMenu.setFont(self.win.getFont())

        count = 0
        for theme in self.win.themes:
            if theme[0] == self.win.configTheme:
                idx = count

            if theme[1] != "":
                self.themeMenu.addItem(QIcon(theme[1]), theme[0])
            else:
                self.themeMenu.addItem(theme[0])
            count += 1

        self.themeMenu.setCurrentIndex(idx)
        self.themeMenu.setGeometry(110, 50, 250, 24)
        self.themeMenu.setStyleSheet(self.win.themeStyle.settingsMenuStyle)
        self.themeMenu.currentTextChanged.connect(self.win.changeTheme)

        self.directoryButton = QPushButton(self)
        self.directoryButton.setIcon(QIcon(self.win.getIconPath("folder")))
        self.directoryButton.setToolTip('Open the Themes Directory')
        self.directoryButton.setGeometry(366, 50, 24, 24)
        self.directoryButton.setIconSize(QSize(24, 24))
        self.directoryButton.setStyleSheet("QPushButton {border: 0; background: transparent;} QPushButton::hover {padding-left: 1px; padding-top: 1px}")
        self.directoryButton.clicked.connect(self.openThemesDirectory)


        label = QLabel(text2html(f"§fClient:", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(20, 81)
        
        
        self.clientMenu = QComboBox(self)
        self.clientMenu.setFont(self.win.getFont())

        count = 0
        for client in self.win.clients:
            if client[0] == self.win.configClient:
                idx = count

            if client[1] != "":
                self.clientMenu.addItem(QIcon(client[1]), client[0])
            else:
                self.clientMenu.addItem(client[0])
            count += 1

        self.clientMenu.setCurrentIndex(idx)
        self.clientMenu.setGeometry(110, 81, 280, 24)
        self.clientMenu.setStyleSheet(self.win.themeStyle.settingsMenuStyle)
        self.clientMenu.currentTextChanged.connect(self.changeClient)


        label = QLabel(text2html(f"§fLogs:", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(20, 112)

        self.customPathBox = QLineEdit(self)
        self.customPathBox.setFont(self.win.getFont())
        self.customPathBox.setMaxLength(36)
        self.customPathBox.setStyleSheet(self.win.themeStyle.settingsLogPathStyle)
        self.customPathBox.setPlaceholderText('...\\'+'\\'.join(self.win.configLogPath.split('\\')[-3:]))
        self.customPathBox.setGeometry(110, 112, 250, 24)
        self.customPathBox.setEnabled(False)

        self.logsButton = QPushButton(self)
        self.logsButton.setIcon(QIcon(self.win.getIconPath("folder")))
        self.logsButton.setToolTip('Choose a log file')
        self.logsButton.setGeometry(366, 112, 24, 24)
        self.logsButton.setIconSize(QSize(24, 24))
        self.logsButton.setStyleSheet("QPushButton {border: 0; background: transparent;} QPushButton::hover {padding-left: 1px; padding-top: 1px}")
        self.logsButton.clicked.connect(self.openLogsFile)


        label = QLabel(text2html(f"§fOpacity:", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(20, 143)
        
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(110, 135, 250, 24)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickInterval(10)
        self.slider.setValue(int(self.win.configOpacity*100))
        self.slider.valueChanged.connect(self.opacityChanged)
        self.slider.sliderPressed.connect(self.sliderPressed)
        self.slider.sliderReleased.connect(self.sliderReleased)
        self.slider.setStyleSheet(self.win.themeStyle.sliderStyle)
        
        
        self.RPCswitch = QCheckBox(self)
        self.RPCswitch.setGeometry(20, 165, 40, 40)
        self.RPCswitch.setToolTip("Show that you are using the overlay in Discord")
        self.RPCswitch.setStyleSheet(self.win.themeStyle.switchButtonStyle)

        if self.win.RPC:
            if self.win.RPC == -1:
                self.RPCswitch.setChecked(False)
            else:
                self.RPCswitch.setChecked(True)
        else:
            self.RPCswitch.setChecked(False)
            self.RPCswitch.setDisabled(True)

        self.RPCswitch.stateChanged.connect(self.RPCUpdate)
        
        
        label = QLabel(text2html(f"§fDiscord Activity", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(60, 175)


        self.STATUSswitch = QCheckBox(self)
        self.STATUSswitch.setGeometry(20, 190, 40, 40)
        self.STATUSswitch.setToolTip("Show your Hypixel stats in Discord")
        self.STATUSswitch.setStyleSheet(self.win.themeStyle.switchButtonStyle)

        if not self.win.RPC or self.win.RPC == -1:
            self.STATUSswitch.setDisabled(True)
        else:
            if self.win.configStatus:
                self.STATUSswitch.setChecked(True)
            else:
                self.STATUSswitch.setChecked(False)

        self.STATUSswitch.stateChanged.connect(self.STATUSUpdate)

        label = QLabel(text2html(f"§fShow Status", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(60, 200)


        self.Whoswitch = QCheckBox(self)
        self.Whoswitch.setGeometry(20, 215, 40, 40)
        self.Whoswitch.setToolTip("Automatically send a /who command when you join a game")
        self.Whoswitch.setStyleSheet(self.win.themeStyle.switchButtonStyle)

        if self.win.configWho:
            self.Whoswitch.setChecked(True)
        else:
            self.Whoswitch.setChecked(False)

        self.Whoswitch.stateChanged.connect(self.WhoUpdate)

        label = QLabel(text2html(f"§fAuto Who", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(60, 225)


        self.globalBlswitch = QCheckBox(self)
        self.globalBlswitch.setGeometry(20, 240, 40, 40)
        self.globalBlswitch.setToolTip("Toggle the Polsu blacklist")
        self.globalBlswitch.setStyleSheet(self.win.themeStyle.switchButtonStyle)

        if self.win.configGlobalBlacklist:
            self.globalBlswitch.setChecked(True)
        else:
            self.globalBlswitch.setChecked(False)

        self.globalBlswitch.stateChanged.connect(self.GlobalBlUpdate)

        label = QLabel(text2html(f"§fPolsu Blacklist", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(60, 250)


        self.blacklistButton = QPushButton(self)
        self.blacklistButton.setIcon(QIcon(self.win.getIconPath("folder")))
        self.blacklistButton.setToolTip("Browse the local blacklists")
        self.blacklistButton.setGeometry(366, 240, 24, 24)
        self.blacklistButton.setIconSize(QSize(24, 24))
        self.blacklistButton.setStyleSheet("QPushButton {border: 0; background: transparent;} QPushButton::hover {padding-left: 1px; padding-top: 1px}")
        self.blacklistButton.clicked.connect(self.openLocalBlacklistFile)


        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon(self.win.getIconPath("exit")))
        self.closeButton.setToolTip('Close the Settings')
        self.closeButton.setGeometry(400, 15, 24, 24)
        self.closeButton.setIconSize(QSize(24, 24))
        self.closeButton.setStyleSheet(self.win.themeStyle.sideBarSmallButtonsStyle)
        self.closeButton.clicked.connect(self.close_settings)

        self.win.setMinimumSize(self.win.width(), self.win.height())
        self.win.setMaximumSize(self.win.width(), self.win.height())

        self.SIGNALS = WidgetSignals()


    def changeClient(self, value: str) -> None:
        """
        Change the client
        
        :param value: The new client
        """
        for client in self.win.clients:
            if client[0] == value:
                self.win.logs.oldString = ""

                path = client[2].format(getuser())

                for c in self.win.clients:
                    if c[2] == str(path).replace("\\", "\\\\"):
                        self.customPathBox.setPlaceholderText("")
                        return self.openLogsFile()

                self.win.configClient = value
                self.win.settings.update("client", value)
                self.win.settings.update("logPath", path)
                self.win.configLogPath = path
                self.customPathBox.setPlaceholderText('...\\'+'\\'.join(self.win.configLogPath.split('\\')[-3:]))
        

    def sliderReleased(self) -> None:
        """
        When the slider is released
        """
        self.win.menu.show()
        
        self.opacity = 0.8
        self.update()


    def sliderPressed(self) -> None:
        """
        When the slider is pressed
        """
        self.win.menu.hide()

        self.opacity = 0
        self.update()


    def opacityChanged(self, value: int) -> None:
        """
        When the slider value is changed
        
        :param value: The new value
        """
        self.win.configOpacity = value/100
        self.win.settings.update("opacity", self.win.configOpacity)
        updateComponents(self.win)


    def STATUSUpdate(self) -> None:
        """
        Update the status
        """
        if self.STATUSswitch.isChecked():
            self.win.settings.update("status", True)
            self.win.configStatus = True

            self.win.notif.send(
                title="Disabled In Game Discord Status",
                message="Your in game status isn't updating anymore."
            )
        else:
            self.win.settings.update("status", False)
            self.win.configStatus = False

            self.win.notif.send(
                title="Enabled In Game Discord Status",
                message="Your in game status is now being displayed."
            )

        if self.win.RPC and not isinstance(self.win.RPC, int):
            self.win.RPC.setConfigStatus(self.win.configStatus)


    def RPCUpdate(self) -> None:
        """
        Update the RPC
        """
        if self.RPCswitch.isChecked():
            self.win.settings.update("RPC", True)
            startRPC(self.win)

            self.STATUSswitch.setDisabled(False)
        else:
            self.win.settings.update("RPC", False)

            self.STATUSswitch.setDisabled(True)

            # If you close Discord when the program is running the overlay crashes.
            try:
                self.win.RPC.disconnect()
            except:
                pass

            self.win.notif.send(
                title="Discord Activity Status Disconnected",
                message="Your Discord status isn't updating anymore."
            )


    def hideupdate(self) -> None:
        """
        Update the hideOverlay
        """
        if self.hideswitch.isChecked():
            self.win.settings.update("hideOverlay", True)
            self.win.configHide = True
        else:
            self.win.settings.update("hideOverlay", False)
            self.win.configHide = False


    def WhoUpdate(self) -> None:
        """
        Update the Who
        """
        if self.Whoswitch.isChecked():
            self.win.configWho = True
            self.win.settings.update("who", True)
        else:
            self.win.configWho = False
            self.win.settings.update("who", False)


    def GlobalBlUpdate(self) -> None:
        """
        Update the Who
        """
        if self.globalBlswitch.isChecked():
            self.win.configGlobalBlacklist = True
            self.win.settings.update("globalBlacklist", True)
        else:
            self.win.configGlobalBlacklist = False
            self.win.settings.update("globalBlacklist", False)


    def openLocalBlacklistFile(self) -> None:
        """
        Open the local blacklist file
        """
        self.close_settings()

        webbrowser.open(self.win.blacklistConfig)
        self.win.mini()


    def openLogsFile(self) -> None:
        """
        Open the logs file
        """
        dialog = QFileDialog(self)
        dialog.setDirectory(r"/".join(self.win.configLogPath.split("\\")[0:-1]))
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Logs (*.log)")
        dialog.setViewMode(QFileDialog.Detail)
        
        if dialog.exec():
            filename = dialog.selectedFiles()[0].replace("/", "\\")
            self.win.settings.update("logPath", filename)
            self.win.configLogPath = filename
            self.customPathBox.setPlaceholderText('...\\'+'\\'.join(self.win.configLogPath.split('\\')[-3:]))

            self.win.configClient = "Custom"
            self.win.settings.update("client", "Custom")

            count = 0
            for client in self.win.clients:
                if client[0] == self.win.configClient:
                    idx = count

                count += 1

            self.clientMenu.setCurrentIndex(idx)


    def openThemesDirectory(self) -> None:
        """
        Open the themes directory
        """
        self.close_settings()

        webbrowser.open(self.win.dirThemes)
        self.win.mini()


    def close_settings(self) -> None:
        """
        Close the Settings Widget
        """
        self.win.setMinimumSize(680, 150)

        width = []
        height = []
        for displayNr in range(QDesktopWidget().screenCount()):
            sizeObject = QDesktopWidget().screenGeometry(displayNr)
            width.append(sizeObject.width())
            height.append(sizeObject.height())
         
        self.win.setMaximumSize(sum(width), sum(height))

        self.win._settingsMenuOpened = False
        self.close()


    def paintEvent(self, event) -> None:
        """
        Paint the Settings Widget
        
        :param event: The event
        """
        return menuPaintEvent(self, self.opacity)


class Info(QWidget):
    """
    Info Widget
    """
    def __init__(self, win) -> None:
        """
        Initialise the Info Widget
        
        :param win: The Overlay window
        """
        super(Info, self).__init__(win)
        self.win = win


        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon(self.win.getIconPath("exit")))
        self.closeButton.setToolTip('Close the Help')
        self.closeButton.setGeometry(400, 15, 24, 24)
        self.closeButton.setIconSize(QSize(24, 24))
        self.closeButton.setStyleSheet(self.win.themeStyle.sideBarSmallButtonsStyle)
        self.closeButton.clicked.connect(self.close_info)

        label = QLabel(text2html(f"§fPolsu Overlay §7v{__version__}", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(125, 10)

        label = QLabel(text2html(f"§fThis overlay was made by Polsulpicien"), self)
        label.setFont(self.win.getFont())
        label.move(20, 40)

        label = QLabel(text2html(f"§f(§9Polsulpicien§f) and is entirely made"), self)
        label.setFont(self.win.getFont())
        label.move(20, 60)

        label = QLabel(text2html(f"§fin Python."), self)
        label.setFont(self.win.getFont())
        label.move(20, 80)

        label = QLabel(text2html(f"§f100% Free to use!", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(115, 80)


        label = QLabel(text2html(f"§fThis Overlay is open-source on §7Github§f."), self)
        label.setFont(self.win.getFont())
        label.move(20, 120)


        label = QLabel(text2html(f"§fAll information is stored only on your", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(20, 160)

        label = QLabel(text2html(f"§fcomputer. No one else has access to", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(20, 180)

        label = QLabel(text2html(f"§fyour settings!", bold=True), self)
        label.setFont(self.win.getFont())
        label.move(20, 200)


        label = QLabel(text2html(f"§fSaved at:"), self)
        label.setFont(self.win.getFont())
        label.move(20, 230)

        label = QLabel(text2html(f"§0/home/{'*' * len(getuser())}/Polsu/ ", bold=True), self)
        label.setFont(self.win.getFont())
        label.move((50), 250)

        directoryButton = QPushButton(self)
        directoryButton.setIcon(QIcon(self.win.getIconPath("folder")))
        directoryButton.setToolTip('Open the settings directory')
        directoryButton.setGeometry(20, 248, 24, 24)
        directoryButton.setIconSize(QSize(24, 24))
        directoryButton.setStyleSheet("QPushButton {border: 0; background: transparent;} QPushButton::hover {padding-left: 1px; padding-top: 1px}")
        directoryButton.clicked.connect(self.openSettingsDirectory)

        self.SIGNALS = WidgetSignals()

    
    def openSettingsDirectory(self) -> None:
        """
        Open the settings directory
        """
        webbrowser.open(self.win.dirConfig)
        self.win.mini()


    def close_info(self) -> None:
        """
        Close the Info Widget
        """
        self.win._infoMenuOpened = False
        self.close()


    def paintEvent(self, event) -> None:
        """
        Paint the Info Widget
        
        :param event: The event
        """
        return menuPaintEvent(self)


    def _onclose(self) -> None:
        """
        Close the Info Widget
        """
        self.SIGNALS.CLOSE.emit()
