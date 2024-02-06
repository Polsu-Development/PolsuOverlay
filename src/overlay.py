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
from .PolsuAPI import User
from src import Menu, Notif, Settings, Logs, Player, loadThemes, openSettings, __version__, DEV_MODE
from .components.theme import ThemeStyle
from .components.logger import Logger
from .components.rpc import openRPC, startRPC
from .components.components import setupComponents, updateComponents, updateGeometry
from .components.reward import closeRewards
from .components.plugins import PluginCore
from .components.blacklist import Blacklist
from .plugins.blacklist import PluginBlacklist
from .plugins.notification import PluginNotification
from .plugins.table import PluginTable
from .plugins.logs import PluginLogs
from .plugins.api import PluginAPI
from .plugins.settings import PluginSettings
from .plugins.window import PluginWindow
from .plugins.player import PluginPlayer
from .utils.path import resource_path
from .utils.log import LoginWorker, LogoutWorker
from .utils.colours import setColor


from PyQt5.QtWidgets import QWidget, QInputDialog
from PyQt5.QtCore import Qt, QRectF, QEvent, QTimer, QVariantAnimation, QAbstractAnimation, QEventLoop
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QPainterPath, QBrush, QFontDatabase, QFont


import os
import webbrowser
import json
import traceback
import pypresence

from pystray import Icon, Menu as Mn, MenuItem
from PIL import Image
from time import time
from datetime import datetime, timedelta
from getpass import getuser
from functools import partial


class Overlay(QWidget):
    """
    Overlay, main class
    """
    def __init__(self, logger: Logger) -> None:
        """
        Initialise the overlay
        
        :param logger: The logger
        """
        super().__init__(flags=Qt.WindowType.WindowStaysOnTopHint)
        self.logger = logger

        self._menuOpened = False
        self._rewardsOpened = False
        self._settingsMenuOpened = False
        self._infoMenuOpened = False
        self._apiKeyMenuOpened = False
        self._mousePressed = False
        self._maximized = False

        self._cornerRadius = 8.0
        self.POPUPWIDTH = 245
        self.overlayTimer = 0
        self.RPCTimer = 0

        self.launch = int(time())
        self.threads = {}

        self.quickbuyWindow = None
        self.win = False
        self.reward = None
        self.auto_minimize = False
        self.RPC = None
        self.user = None
        self.tray = None
        self.blacklist: Blacklist = None


        if DEV_MODE:
            self.logger.warning("You are running the overlay in development mode!")

        # Assets
        self.pathAssets = resource_path('assets')
        self.logger.debug(f"Assets path: {self.pathAssets}")

        self.pathThemes = resource_path('themes')
        self.logger.debug(f"Themes path: {self.pathThemes}")


        # Load Settings
        self.logger.debug("Loading the Settings...")
        self.settings = Settings(self)
        conf = self.settings.loadConfig()
        self.logger.debug(f"Settings: {conf}")


        # Player
        self.logger.debug("Loading the Player...")
        self.player = Player(self)
        self.logger.debug(f"Player {'loaded' if self.player.client else 'not loaded'}.")


        # Notif
        self.logger.debug("Loading the Notifications...")
        self.notif = Notif(f"{self.pathAssets}/polsu/Polsu_.ico")
        self.minimizeNotif = True
        self.logger.debug(f"Notifications enabled.")


        # Logs
        self.logger.debug("Loading the Logs...")
        self.logs = Logs(self)
        self.logs.readLogFile()
        self.logger.debug(f"Logs enabled.")


        # Themes
        self.logger.debug("Loading the Themes...")
        loadThemes(self)
        self.loadThemes = loadThemes
        self.changeTheme(self.configTheme, False)
        self.logger.debug(f"Theme: {self.themeStyle.name}")


        # Fonts
        self.minecraftFont = QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(f"{self.pathAssets}/fonts/minecraft-font.ttf"))[0])
        self.logger.debug(f"Loaded font: {self.pathAssets}/fonts/minecraft-font.ttf")


        # Clients
        self.logger.debug("Loading the Clients...")
        self.loadClients()
        self.logger.debug(f"Clients: {self.clients}")


        # Discord RPC
        self.logger.debug("Loading the Discord RPC...")
        if self.configRPC:
            startRPC(self)
        else:
            # Checking if the RPC is enabled or not (in order to enable the button in the settings menu)
            openRPC(self)

            self.logger.debug(f"Discord RPC: {self.RPC}")


        # Check Logs Task
        self.logger.debug("Loading the Check Logs Task...")
        checkLogsTask = QTimer(self)
        checkLogsTask.setInterval(700) #1000 -> 1 sec | 0.7 sec
        checkLogsTask.timeout.connect(self.logs.task)
        checkLogsTask.start()
        self.logger.debug(f"Check Logs Task active: {'yes' if checkLogsTask.isActive() else 'no'}")


        # Timer
        self.logger.debug("Loading the Timer...")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showGameTime)
        self.timer.start(1000)
        self.logger.debug(f"Timer active: {'yes' if self.timer.isActive() else 'no'}")


        # Setup
        self.logger.debug("Setting up the Overlay...")
        self.setupWindow()
        self.logger.debug("Overlay setup completed!")


        # Login
        self.logger.debug(f"Loading the API Key...")
        if self.configAPIKey != "":
            self.logger.info("Logging in...")

            try:
                self.threads["login"] = LoginWorker(self.configAPIKey, self.logger)
                self.threads["login"].ended.connect(self.loginEnded)
                self.threads["login"].start()
            except:
                self.logger.error(f"An error occurred while logging in!\nTraceback: {traceback.format_exc()}")

            self.login = True
        else:
            self.logger.warning("No API Key found!")
            self.login = False

            if not self._apiKeyMenuOpened:
                openSettings(self)


        self.logger.info("Polsu Overlay is running!")

        # Plugins
        self.logger.debug("Loading the Plugins...")
        self.plugins = PluginCore(
            self.logger,
            PluginBlacklist(self.blacklist),
            PluginNotification(self.notif),
            PluginTable(self.table),
            PluginLogs(self.logs),
            PluginAPI(self.player.client),
            PluginSettings(self.settings),
            PluginWindow(self.ask),
            PluginPlayer(self.player),
        )
        self.plugins.load_plugins(self.pluginsConfig)
        self.logger.info(f"There are {len(self.plugins.getPlugins())} plugins loaded.")
        self.logger.debug(f"Plugins: {', '.join([plugin.__name__ for plugin in self.plugins.getPlugins()])}")
        self.logger.debug("Plugins loaded!")

    def setTitleBarVisible(self, visible):
        if not visible:
            self.setWindowFlags(Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(Qt.Window)
        self.show()

    def loginEnded(self, user: User) -> None:
        """
        Called when the login thread ends
        
        :param user: The user
        """
        if user:
            self.logger.info(f"Logged in as: {user.username} ({user.uuid})")
            self.user = user

            self.plugins.broadcast("on_login", user)

            self.player.loadPlayer(user.username, user.uuid)


    def ask(self, title: str, message: str) -> str:
        """
        Ask the user a question
        """
        dialog = QInputDialog(self)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle(title)
        dialog.setLabelText(message)
        dialog.setWindowOpacity(100)
        dialog.setAttribute(Qt.WA_TranslucentBackground, False)
        dialog.setStyleSheet("background: white")
        dialog.setFixedSize(400, 100)

        if dialog.exec_():
            return dialog.textValue()
        else:
            return ""


    def showGameTime(self):
        self.RPCTimer += 1
        if self.RPCTimer > 3:
            if self.configRPC and self.RPC is not None and not isinstance(self.RPC, int):
                try:
                    self.RPC.update()
                except (RuntimeWarning, RuntimeError):
                    pass
                except pypresence.exceptions.PipeClosed:
                    # Try to reconnect
                    self.RPC.disconnect()
                    startRPC(self)
                except:
                    self.RPC.disconnect()
                    self.logger.error(f"An error occurred while updating the Discord RPC!\nTraceback: {traceback.format_exc()}")
                    self.RPC = None
            else:
                openRPC(self)

            self.RPCTimer = 0

        if self.configAPIKey == "":
            if not self._apiKeyMenuOpened:
                openSettings(self)
        else:
            if not self.login:
                try:
                    self.threads["login"] = LoginWorker(self.configAPIKey, self.logger)
                    self.threads["login"].ended.connect(self.loginEnded)
                    self.threads["login"].start()
                except:
                    self.logger.error(f"An error occurred while logging in!\nTraceback: {traceback.format_exc()}")

                self.login = True

        self.overlayTimer += 1
        self.timerBox.updateToolTip()
        self.timerIcon.updateToolTip()

        for y in range(self.table.rowCount()):
            for x in range(0, self.table.columnCount()):
                __item = self.table.item(y, x)

                if __item:
                    data = __item.data(Qt.UserRole)
                    if data:
                        if data == 1:
                            if __item.background().color() != QColor("transparent"):
                                anim = QVariantAnimation(
                                    self,
                                    duration=1000,
                                    startValue=QColor(self.themeStyle.table_highlight),
                                    endValue=QColor("transparent")
                                )
                                anim.valueChanged.connect(partial(setColor, __item))
                                anim.start(QAbstractAnimation.DeleteWhenStopped)
                                
                                __item.setData(Qt.UserRole, None)
                        elif data == 2:
                            __item.setData(Qt.UserRole, __item.data(Qt.UserRole) - 1)


        # FIXME: Automatically minimize the overlay causes the task to freeze

        #if not self.logs.hideOverlay and self.auto_minimize and self.isMinimized():
        #    self.auto_minimize = False
        #    self.showNormal()


        if self.logs.isInGame:
            diff = datetime.now() - self.logs.gameStart
            self.timerBox.setText(str(timedelta(seconds=int(diff.total_seconds()))))
            self.timerBox.update()

            if self.logs.timeIconIndex == 0:
                self.timerIcon.setIcon(QIcon(self.timeIconsCache[0]))
            elif self.logs.timeIconIndex == 1:
                self.timerIcon.setIcon(QIcon(self.timeIconsCache[1]))
            elif self.logs.timeIconIndex == 2:
                self.timerIcon.setIcon(QIcon(self.timeIconsCache[2]))

            self.logs.timeIconIndex += 1
            if self.logs.timeIconIndex > 2:
                self.logs.timeIconIndex = 0

            #if self.logs.hideOverlay:
            #    self.logs.hideOverlayTimer += 1
            #    if self.logs.hideOverlayTimer == 15:
            #        self.logs.hideOverlayTimer = -1
            #        self.auto_minimize = True
            #        self.showMinimized()


    def loadClients(self):
        self.clients = []

        with open(f"{self.pathAssets}/clients/data.json", "r") as f:
            clientsData = json.load(f)

        added = False
        for client in os.listdir(f"{self.pathAssets}/clients"):
            path = clientsData.get(client[0:-4], "")
            icon = f"{self.pathAssets}/clients/{client}"

            if client.endswith(".png"):
                if path == "":
                    if self.configClient == "Custom":
                        path = self.configLogPath

                    self.clients.append((client[0:-4], icon, path))
                else:
                    if os.path.exists(path.format(getuser())):
                        self.clients.append((client[0:-4], icon, path))
                        added = True
        
        if not added:
            self.notif.send(
                title="Warning!",
                message="Couldn't find any Minecraft Clients.\nGo to: Settings -> Client -> Custom, and choose a log path.",
                block=True
            )


    def setupWindow(self) -> None:
        """
        Setup the overlay window
        """
        setupComponents(self)

        self.setWindowTitle("Polsu Overlay")
        self.setWindowIcon(QIcon(f"{self.pathAssets}/polsu/Polsu_.png"))

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitleBarVisible(False)

        self.setStyleSheet("background: transparent")

        self.setGeometry(self.configXY[0], self.configXY[1], self.configWH[0], self.configWH[1])
        self.setMinimumSize(880, 150)

        self.central_widget = QWidget()
        #self.setCentralWidget(self.central_widget)

        updateComponents(self)


    def getIconPath(self, item: str, path: str = None) -> str:
        """
        Get the icon path of an item
        
        :param item: The item
        :param path: The path of the theme
        :return: The icon path
        """
        if not path:
            path = self.themeStyle.path

        if os.path.exists(f"{path}/icons/{item}.png"):
            return f"{path}/icons/{item}.png"
        else:
            if os.path.exists(f"{path}/icons/{item}.svg"):
                return f"{path}/icons/{item}.svg"
            else:
                return f"{self.pathAssets}/icons/{item}.svg"


    def getFont(self, path: str = None) -> QFont:
        """
        Get the font

        :param path: The path of the theme
        :return: The font
        """
        if not path:
            path = self.themeStyle.path
            
        if os.path.exists(f"{path}/font.ttf"):
            return QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(f"{path}/font.ttf"))[0])
        else:
            return self.minecraftFont
    

    def changeTheme(self, value, update: bool = True):
        if update:
            self.configTheme = value
            self.settings.update("theme", self.configTheme)
            
        self.themeStyle = ThemeStyle(self, value)
        
        self.timeIconsCache = [
            self.getIconPath("hourglass-start"),
            self.getIconPath("hourglass-half"),
            self.getIconPath("hourglass-end")
        ]

        if update:
            updateComponents(self)

            if self._menuOpened:
                self.open_menu()
                self.open_menu()
                self.menu.openSettings()


    def show_window(self):
        self.auto_minimize = False
        self.tray.visible = False
        self.tray.stop()

        self.showNormal()


    def destroy_window(self):
        self.tray.visible = False
        self.tray.stop()

        self.close()


    def open_menu(self):
        if self.configAPIKey == "":
            if self.apikeymenu.settingsMenu:
                self.apikeymenu.settingsMenu.apikeyBox.setFocus()
                self.apikeymenu.settingsMenu.apikeyBox.setStyleSheet(self.themeStyle.settingsAPIKeyFocus)
                
                loop = QEventLoop()
                QTimer.singleShot(1000, loop.quit)
                loop.exec_()
                
                try:
                    self.apikeymenu.settingsMenu.apikeyBox.setStyleSheet(self.themeStyle.settingsAPIKeyStyle)
                except:
                    pass

            self.notif.send(
                title="Warning!",
                message="You have not entered your API Key yet.",
            )
        else:
            if self._apiKeyMenuOpened:
                self.close_apikey_menu()

            if self._rewardsOpened:
                closeRewards(self)

            if not self._menuOpened:
                self.menu = Menu(self)
                self.menu.move(0, 34)
                self.menu.resize(self.width(), self.height())
                self.menu.SIGNALS.CLOSE.connect(self.close_menu)
                self._menuOpened = True
                self.menu.show()

                self.searchBox.setEnabled(False)
                self.searchIcon.setEnabled(False)

                if self._settingsMenuOpened:
                    self._settingsMenuOpened = False
                    self.menu.openSettings()

                if self._infoMenuOpened:
                    self._infoMenuOpened = False
                    self.menu.openInfo()
            else:
                if self._settingsMenuOpened:
                    self.menu.close_settingsMenu(disable=False)

                if self._infoMenuOpened:
                    self.menu.close_infoMenu(disable=False)
                
                self.close_menu()


    def close_menu(self):
        self.menu.close()
        self._menuOpened = False

        self.searchBox.setEnabled(True)
        self.searchIcon.setEnabled(True)


    def close_apikey_menu(self):
        if self._apiKeyMenuOpened:
            if self.apikeymenu.settingsMenu:
                self.apikeymenu.settingsMenu.close_settings()
            self.apikeymenu.close()
            self._apiKeyMenuOpened = False

            self.searchBox.setEnabled(True)
            self.searchIcon.setEnabled(True)


    ##############################################
    #                                            #
    #  Events                                    #
    #                                            #
    ##############################################
    def changeEvent(self, event) -> None:
        """
        Called when the window state changes
        
        :param event: The event
        """
        if event.type() == QEvent.WindowStateChange:
            # self.win is to check if the minimize event was launched by the window or not
            if int(event.oldState()) == 0 and int(self.windowState()) == 1 and not self.win:
                self.mini()
            elif event.oldState() == Qt.WindowMinimized and self.windowState() == Qt.WindowNoState:
                self.show_window()
            elif int(event.oldState()) == 3 and self.windowState() == Qt.WindowFullScreen:
                self.show_window()


    def resizeEvent(self, event) -> None:
        """
        Called when the window is resized
        
        :param event: The event
        """
        updateGeometry(self)

        if not self.window().isFullScreen():
            self.settings.update("wh", [self.width(), self.height()])


    def maxi(self) -> None:
        """
        Maximise the window
        """
        if not self._apiKeyMenuOpened:
            if self.window().isFullScreen():
                self.window().showNormal()
            else:
                self.window().showFullScreen()
                
            updateGeometry(self)


    def mini(self) -> None:
        """
        Minimise the window
        """
        self.win = True
        self.showMinimized()
        self.window().showMinimized()
        self.win = False
        
        if self.quickbuyWindow is not None:
            self.quickbuyWindow.window().showMinimized()

        if not self.minimizeNotif:
            self.notif.send(
                title="Minimized",
                message="Hey, the overlay is now minimized in your applications tray."
            )

            self.minimizeNotif = True

        if self.tray is None or not self.tray._running:
            self.tray = Icon(
                name = 'polsu', 
                icon = Image.open(f"{self.pathAssets}/polsu/Polsu_.ico"),
                title = f"Polsu Overlay v{__version__}",
                menu = Mn(
                    MenuItem(
                        text=f"Polsu Overlay",
                        action=lambda: webbrowser.open('https://overlay.polsu.xyz'),
                        default=False,
                        visible=True,
                        enabled=False,
                        
                    ),
                    Mn.SEPARATOR,
                    MenuItem(
                        text="Github",
                        action=lambda: webbrowser.open('https://github.com/PolsuDevelopment'),
                        default=False,
                        visible=True
                    ),
                    MenuItem(
                        text="Website",
                        action=lambda: webbrowser.open('https://polsu.xyz'),
                        default=False,
                        visible=True
                    ),
                    MenuItem(
                        text="Discord",
                        action=lambda: webbrowser.open('https://discord.polsu.xyz'),
                        default=False,
                        visible=True
                    ),
                    Mn.SEPARATOR,
                    Mn.SEPARATOR,
                    MenuItem(
                        text="Show",
                        action=self.show_window,
                        default=True,
                        visible=True
                    ),
                    MenuItem(
                        text="Quit",
                        action=self.destroy_window,
                        default=False,
                        visible=True
                    )
                )
            )

            self.tray.run()


    def paintEvent(self, event) -> None:
        """
        Called when the window is painted
        
        :param event: The event
        """
        x = -1
        y = -1
        width = self.size().width()
        height = 36

        painter = QPainter(self)
        painter.setPen(QPen(QColor(self.themeStyle.color), 2))
        painter.setBrush(QBrush(QColor(self.themeStyle.color)))
        painter.setOpacity(self.configOpacity)
        painter.setRenderHints(QPainter.Antialiasing)


        path = QPainterPath()
        rect = self.rect()
        path.addRoundedRect(QRectF(rect), self._cornerRadius, self._cornerRadius)
        painter.drawPath(path)
        

        painter.setPen(QPen(QColor(self.themeStyle.color), 1))

        c = self.configOpacity+0.5
        if c > 0.8:
            c = 0.8
        painter.setOpacity(c)

        path = QPainterPath()
        path.moveTo(x + self._cornerRadius, y)
        path.arcTo(x, y, 2 * self._cornerRadius, 2 * self._cornerRadius, 90.0, 90.0)
        path.lineTo(x, height)
        path.lineTo(width, height)
        if self._cornerRadius == 0:
            path.lineTo(width, y)
        path.arcTo(x + (width - 2 * self._cornerRadius), y, 2 * self._cornerRadius, 2 * self._cornerRadius, 0.0, 90.0)
        painter.drawPath(path)


        painter.setOpacity(c-0.1)
        painter.drawRect(x, 36, width, 1)

        painter.end()

        
    def mousePressEvent(self, event) -> None:
        """
        Called when the mouse is pressed
        
        :param event: The event
        """
        self._mousePressed = True
        self._mousePos = event.globalPos()
        self._windowPos = self.pos()
        self._mouseY = event.y()


    def mouseMoveEvent(self, event) -> None:
        """
        Called when the mouse is moved
        
        :param event: The event
        """
        if self._mousePressed and self._mouseY < 36:
            if bool(self.windowState() & Qt.WindowMaximized):
                self.setWindowState(Qt.WindowNoState)

            self.move(self._windowPos + (event.globalPos() - self._mousePos))


    def mouseReleaseEvent(self, event) -> None:
        """
        Called when the mouse is released
        
        :param event: The event
        """
        self._mousePressed = False

        rect = self.geometry()

        if rect.y() < 0:
            difference = abs(0-rect.y())
            rect.setY(0)
            rect.setHeight(rect.height() + difference)
            self.setGeometry(rect)

        self.settings.update("xy", [self.x(), self.y()])


    def mouseDoubleClickEvent(self, event) -> None:
        """
        Called when the window is double clicked

        :param event: The event
        """
        if event.y() < 36:
            self.maxi()

            if self._menuOpened:
                self.menu.resize(self.width(), self.height())


    def closeEvent(self, event) -> None:
        """
        Called when the window is closed
        
        :param event: The event
        """
        if hasattr(self, "tray") and self.tray:
            self.tray.visible = False
            self.tray.stop()

        if self.quickbuyWindow is not None:
            self.quickbuyWindow.close()

        event.accept()

        if self.configAPIKey != "":
            self.setCursor(Qt.WaitCursor)

            self.logger.info("Logging out...")

            try:
                self.threads["logout"] = LogoutWorker(self.configAPIKey, self.launch, self.logger)
                self.threads["logout"].start()
                self.threads["logout"].wait()
            except:
                self.logger.error(f"An error occurred while logging out!\nTraceback: {traceback.format_exc()}")


            if self.user:
                self.plugins.broadcast("on_logout", self.user)


        self.plugins.unload_plugins()


        self.logger.info("Polsu Overlay is now closed!")
