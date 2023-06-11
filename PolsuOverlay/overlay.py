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
from PolsuOverlay import Menu, Rewards, Table, Presence, Notif, Settings, Logs, Player, loadThemes, Polsu, __version__
from .components.theme import ThemeStyle
from .components.timer import TimerBox, TimerIcon

from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QLineEdit
from PyQt5.QtCore import Qt, QSize, QRectF, QEvent, QTimer
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QPainterPath, QBrush, QFontDatabase, QFont
from PyQt5.QtWinExtras import QtWin
from pyqt_frameless_window import FramelessMainWindow


import os, sys
import webbrowser
import asyncio
import json

from pystray import Icon, Menu as Mn, MenuItem
from PIL import Image
from threading import Thread
from time import time
from datetime import timedelta
from getpass import getuser


class Overlay(FramelessMainWindow):
    """
    Overlay, main class
    """
    def __init__(self):
        super().__init__(flags=[Qt.WindowStaysOnTopHint])
        self._menuOpened = False
        self._rewardsOpened = False
        self._settingsMenuOpened = False
        self._infoMenuOpened = False
        self._mousePressed = False
        self._maximized = False
        self._cornerRadius = 8.0

        self.POPUPWIDTH = 245

        self.pathAssets = self.resource_path('assets')
        self.pathThemes = self.resource_path('themes')

        # Load Settings
        self.settings = Settings(self)
        self.settings.loadConfig()

        self.logs = Logs(self)

        # Themes
        loadThemes(self)
        self.loadThemes = loadThemes
        self.changeTheme(self.configTheme, False)

        self.launch = int(time())

        self.notif = Notif(f"{self.pathAssets}/polsu/Polsu_.ico")
        self.minimizeNotif = False

        self.minecraftFont = QFont(QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(f"{self.pathAssets}/fonts/minecraft-font.ttf"))[0])
        QFontDatabase.addApplicationFont(f"{self.pathAssets}/fonts/unifont.ttf")
        self.quickbuyWindow = None
        self.win = False
        self.reward = None
        self.overlayTimer = 0

        self.loadClients()
        
        if self.configRPC:
            self.startRPC()
        else:
            try:
                self.RPC = Presence(self.launch)
                self.RPC = -1
            except:
                self.RPC = None

        self.logs.readLogFile()

        self.checkThreadTimer = QTimer(self)
        self.checkThreadTimer.setInterval(700) #1000 -> 1 sec | 0.7 sec
        self.checkThreadTimer.timeout.connect(self.mainTask)
        self.checkThreadTimer.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showGameTime)
        self.timer.start(1000)

        self.setupWindow()


        self.player = Player(self)


    def showGameTime(self):
        self.overlayTimer += 1
        self.timerBox.updateToolTip()
        self.timerIcon.updateToolTip()

        if self.logs.isInGame:
            self.logs.timerCount += 1
            self.timerBox.setText(str(timedelta(seconds=self.logs.timerCount)))
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


    def mainTask(self):
        if self.logs.oldString == "":
            self.logs.readLogFile()
        else:
            try:
                self.logs.readLogs()
            except Exception as e:
                print(e)


    def startRPC(self):
        Thread(target=self.discordRPC, args=(asyncio.new_event_loop(), )).start()


    def discordRPC(self, loop):
        asyncio.set_event_loop(loop)

        try:
            self.RPC = Presence(self.launch)
            self.RPC.connect()

            self.notif.send(
                title="Discord Activity Status Update",
                message="Succesfully connected to Discord!"
            )
        except:
            self.RPC = None
            
            self.notif.send(
                title="Discord Activity Status Error",
                message="Something went wrong, are you sure that your Discord client is opened?"
            )


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


    def setupWindow(self):
        self.setWindowTitle("Polsu Overlay")
        self.setWindowIcon(f"{self.pathAssets}/polsu/Polsu_.png")
        
        self.setTitleBarVisible(False)

        QtWin.enableBlurBehindWindow(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setStyleSheet("background: transparent")
        self.setWindowOpacity(100 / 100)


        self.setGeometry(self.configXY[0], self.configXY[1], self.configWH[0], self.configWH[1])
        self.setMinimumSize(680, 150)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
       

        # Components, title, buttons, search bar...
        self.setupComponents()
        self.updateComponents()


    def setupComponents(self):
        self.menuButton = QPushButton(self)
        self.menuButton.setIcon(QIcon(f"{self.pathAssets}/polsu/Polsu__.png"))
        self.menuButton.setToolTip('Menu')
        self.menuButton.setGeometry(4, 4, 30, 30)
        self.menuButton.setIconSize(QSize(25, 25))
        self.menuButton.clicked.connect(self.open_menu)

        self.overlayTitle = QLabel(self)
        self.overlayTitle.setText("Polsu Overlay")
        self.overlayTitle.setFont(self.minecraftFont)
        self.overlayTitle.setStyleSheet(self.themeStyle.titleStyle)
        self.overlayTitle.adjustSize()
        self.overlayTitle.move(40, 1)

        self.searchBox = QLineEdit(self)
        self.searchBox.setFont(self.minecraftFont)
        self.searchBox.setMaxLength(16)
        self.searchBox.setPlaceholderText("Search...")
        self.searchBox.editingFinished.connect(self.enterPress)

        self.searchIcon = QPushButton(QIcon(self.getIconPath("search")), "", self)
        self.searchIcon.setIconSize(QSize(14, 14))
        self.searchIcon.clicked.connect(lambda: self.searchBox.setFocus())
        self.searchIcon.setStyleSheet("QPushButton::hover {padding-left: 1px; padding-top: 1px}")

        self.timerBox = TimerBox(self)
        self.timerBox.setFont(self.minecraftFont)
        self.timerBox.setText("0:00:00")
        self.timerBox.setEnabled(False)

        self.timerIcon = TimerIcon(QIcon(self.getIconPath("hourglass-start")), "", self)
        self.timerIcon.setIconSize(QSize(14, 14))
        self.timerIcon.setStyleSheet("QPushButton::hover {padding-left: 1px; padding-top: 1px}")

        self.deliveryBox = QLineEdit(self)
        self.deliveryBox.setEnabled(False)

        self.deliverybutton = QPushButton(self)
        self.deliverybutton.setToolTip('Daily Delivery')
        self.deliverybutton.setIconSize(QSize(14, 14))
        self.deliverybutton.clicked.connect(self.openRewards)
        
        self.table = Table(self)

        self.minimizebutton = QPushButton(self)
        self.minimizebutton.setToolTip('Minimize')
        self.minimizebutton.setIconSize(QSize(20, 20))
        self.minimizebutton.clicked.connect(self.mini)

        self.maximizebutton = QPushButton(self)
        self.maximizebutton.setToolTip('Maximize')
        self.maximizebutton.setIconSize(QSize(20, 20))
        self.maximizebutton.clicked.connect(self.maxi)

        self.exitbutton = QPushButton(self)
        self.exitbutton.setToolTip('Quit Overlay')
        self.exitbutton.setIconSize(QSize(30, 30))
        self.exitbutton.clicked.connect(self.close)


    def enterPress(self):
        self.searchBox.setDisabled(True)

        self.player.getPlayer([self.searchBox.text()])

        self.searchBox.setText("")
        self.searchBox.setDisabled(False)


    def getIconPath(self, item, path = None):
        if not path:
            path = self.themeStyle.path

        if os.path.exists(f"{path}/icons/{item}.png"):
            return f"{path}/icons/{item}.png"
        else:
            if os.path.exists(f"{path}/icons/{item}.svg"):
                return f"{path}/icons/{item}.svg"
            else:
                return f"{self.pathAssets}/icons/{item}.svg"


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
            self.updateComponents()

            if self._menuOpened:
                self.open_menu()
                self.open_menu()
                
    
    def updateComponents(self):
        self.menuButton.setStyleSheet(self.themeStyle.buttonsStyle)
        self.menuButton.update()

        self.overlayTitle.setStyleSheet(self.themeStyle.titleStyle)
        self.overlayTitle.update()

        self.searchIcon.setIcon(QIcon(self.getIconPath("search")))
        self.searchIcon.update()

        self.searchBox.setStyleSheet(self.themeStyle.searchBarStyle)
        self.searchBox.update()

        self.timerIcon.setIcon(QIcon(self.getIconPath("hourglass-start")))
        self.timerIcon.update()

        self.timerBox.setStyleSheet(self.themeStyle.timerBarStyle)
        self.timerBox.update()

        self.deliverybutton.setStyleSheet(self.themeStyle.buttonsStyle)
        self.deliverybutton.setIcon(QIcon(self.getIconPath("user")))
        self.deliverybutton.update()

        self.deliveryBox.setStyleSheet(self.themeStyle.timerBarStyle)
        self.deliveryBox.update()
        
        self.table.setStyleSheet(self.themeStyle.tableStyle)
        self.table.VscrollBar.setStyleSheet(self.themeStyle.VscrollBarStyle)
        self.table.HscrollBar.setStyleSheet(self.themeStyle.HscrollBarStyle)

        for i in range(0, self.table.rowCount()):
            for j in range(0, self.table.columnCount()):
                item = self.table.cellWidget(i, j)
                if type(item) == QPushButton and item.property("name") == "dots":
                    item.setIcon(QIcon(self.getIconPath("dots")))
            
        self.table.update()

        self.minimizebutton.setStyleSheet(self.themeStyle.buttonsStyle)
        self.minimizebutton.setIcon(QIcon(self.getIconPath("minimize")))
        self.minimizebutton.update()

        self.maximizebutton.setStyleSheet(self.themeStyle.buttonsStyle)
        self.maximizebutton.setIcon(QIcon(self.getIconPath("maximize")))
        self.maximizebutton.update()

        self.exitbutton.setStyleSheet(self.themeStyle.closeButtonStyle)
        self.exitbutton.setIcon(QIcon(self.getIconPath("close")))
        self.exitbutton.update()

        self.update()


    def updateGeometry(self):
        self.searchIcon.setGeometry(263, 10, 19, 19)
        self.searchBox.setGeometry(260, 8, 170, 23)
        self.timerIcon.setGeometry(443, 10, 19, 19)
        self.timerBox.setGeometry(440, 8, 90, 23)
        self.deliverybutton.setGeometry(541, 9, 20, 20)
        self.deliveryBox.setGeometry(540, 8, 22, 22)
        self.table.setGeometry(5, 45, self.size().width()-10, self.size().height()-50)
        self.minimizebutton.setGeometry(self.size().width() - 94, 4, 30, 30)
        self.maximizebutton.setGeometry(self.size().width() - 64, 4, 30, 30)
        self.exitbutton.setGeometry(self.size().width() - 34, 4, 30, 30)

        if self._rewardsOpened:
            self.openRewards()
            
            if self.height() >= 220:
                self.openRewards()
            

        if self.height() >= 220:
            self.deliverybutton.setEnabled(True)
        else:
            self.deliverybutton.setEnabled(False)

        if self._menuOpened:
            self.open_menu()
            self.open_menu()

            #self.menu.resize(self.width(), self.height())
            self.menu.close_menu.setGeometry(self.POPUPWIDTH, 2, self.width(), self.height())

            if self._settingsMenuOpened:
                if self.width() < self.POPUPWIDTH+430 or self.height() < self.POPUPWIDTH+70:
                    self.menu.close_settingsMenu()
                else:
                    self.menu.settingsMenu.setGeometry(self.POPUPWIDTH, 34, self.width(), self.height())
            if self._infoMenuOpened:
                if self.width() < self.POPUPWIDTH+430 or self.height() < self.POPUPWIDTH+70:
                    self.menu.close_infoMenu()
                else:
                    self.menu.infoMenu.setGeometry(self.POPUPWIDTH, 34, self.width(), self.height())


    def resizeEvent(self, event):
        self.updateGeometry()

        if not self.window().isFullScreen():
            self.settings.update("wh", [self.width(), self.height()])
        
    
    def maxi(self):
        if self.window().isFullScreen():
            self.window().showNormal()
        else:
            self.window().showFullScreen()
            
        self.updateGeometry()


    def mini(self):
        self.win = True
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

        self.tray = Icon(
            name = 'polsu', 
            icon = Image.open(f"{self.pathAssets}/polsu/Polsu_.ico"),
            title = f"Polsu Overlay v{__version__}",
            menu = Mn(
                MenuItem(
                    text=f"Polsu Overlay",
                    action=lambda: webbrowser.open('https://discord.gg/xm9QX3Q'),
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
                    action=lambda: webbrowser.open('https://discord.gg/xm9QX3Q'),
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

    def openRewards(self):
        if self._menuOpened:
            self.open_menu()

        if not self._rewardsOpened:
            self.searchBox.setEnabled(False)
            self.searchIcon.setEnabled(False)

            self.rewards = Rewards(self)
            self.rewards.move(0, 34)
            self.rewards.resize(self.width(), self.height())
            self.rewards.SIGNALS.CLOSE.connect(self.closeRewards)
            self._rewardsOpened = True
            self.rewards.show()
        else:
            self.closeRewards()
        

    def closeRewards(self):
        self.rewards.close()
        self._rewardsOpened = False

        self.searchBox.setEnabled(True)
        self.searchIcon.setEnabled(True)


    def flags(self, status: bool = True):
        self.setAttribute(Qt.WA_TransparentForMouseEvents, status)
        self.setAttribute(Qt.WA_NoChildEventsForParent, status)

        if status:
            self.setWindowFlags(Qt.Window|Qt.X11BypassWindowManagerHint|Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.Window|Qt.WindowStaysOnTopHint)

        self.showNormal()


    def show_window(self):
        self.tray.visible = False
        self.tray.stop()
        self.showNormal()


    def destroy_window(self):
        self.tray.visible = False
        self.tray.stop()

        self.close()


    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            # self.win is to check if the minimize event was launched by the window or not
            if int(event.oldState()) == 0 and int(self.windowState()) == 1 and not self.win:
                self.mini()
            elif event.oldState() == Qt.WindowMinimized and self.windowState() == Qt.WindowNoState:
                self.show_window()
            elif int(event.oldState()) == 3 and self.windowState() == Qt.WindowFullScreen:
                self.show_window()


    def open_menu(self):
        if self._rewardsOpened:
            self.closeRewards()

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

        
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    def paintEvent(self, event):
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

        
    def mousePressEvent(self, event):
        self._mousePressed = True
        self._mousePos = event.globalPos()
        self._windowPos = self.pos()
        self._mouseY = event.y()


    def mouseMoveEvent(self, event):
        if self._mousePressed and self._mouseY < 36:
            if bool(self.windowState() & Qt.WindowMaximized):
                self.setWindowState(Qt.WindowNoState)

            self.move(self._windowPos + (event.globalPos() - self._mousePos))


    def mouseReleaseEvent(self, event):
        self._mousePressed = False

        rect = self.geometry()

        if rect.y() < 0:
            difference = abs(0-rect.y())
            rect.setY(0)
            rect.setHeight(rect.height() + difference)
            self.setGeometry(rect)

        self.settings.update("xy", [self.x(), self.y()])


    def mouseDoubleClickEvent(self, event):
        if event.y() < 36:
            self.maxi()

            if self._menuOpened:
                self.menu.resize(self.width(), self.height())


    def closeEvent(self, event):
        if self.quickbuyWindow is not None:
            self.quickbuyWindow.close()
        
        event.accept()