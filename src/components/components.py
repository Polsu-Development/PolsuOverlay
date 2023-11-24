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
from .table import Table
from .timer import TimerBox, TimerIcon
from .apikey import openSettings
from .reward import openRewards
from ..utils.colours import setColor

from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QSize, QVariantAnimation, QAbstractAnimation
from PyQt5.QtGui import QIcon, QColor
from functools import partial


def setupComponents(win) -> None:
    """
    Setup the components of the overlay
    
    :param win: The Overlay window
    """
    win.menuButton = QPushButton(win)

    if win.themeStyle.icon == "custom":
        count = 0
        for theme in win.themes:
            if theme[0] == win.configTheme:
                idx = count
            count += 1

        if win.themes[idx][1] != "":
            win.menuButton.setIcon(QIcon(win.themes[idx][1]))
        else:
            win.menuButton.setIcon(QIcon(f"{win.pathAssets}/polsu/Polsu__.png"))
    else:
        win.menuButton.setIcon(QIcon(f"{win.pathAssets}/polsu/Polsu__.png"))

    win.menuButton.setToolTip('Menu')
    win.menuButton.setGeometry(4, 4, 30, 30)
    win.menuButton.setIconSize(QSize(25, 25))
    win.menuButton.clicked.connect(win.open_menu)

    win.overlayTitle = QLabel(win)
    win.overlayTitle.setText(win.themeStyle.name)
    win.overlayTitle.setFont(win.minecraftFont)
    win.overlayTitle.setStyleSheet(win.themeStyle.titleStyle)
    win.overlayTitle.adjustSize()
    win.overlayTitle.move(40, 1)

    win.searchBox = QLineEdit(win)
    win.searchBox.setFont(win.minecraftFont)
    win.searchBox.setMaxLength(16)
    win.searchBox.setPlaceholderText("Search...")
    win.searchBox.returnPressed.connect(lambda: enterPress(win))
    win.searchBox.adjustSize()

    win.searchIcon = QPushButton(QIcon(win.getIconPath("search")), "", win)
    win.searchIcon.setIconSize(QSize(14, 14))
    win.searchIcon.clicked.connect(lambda: win.searchBox.setFocus())
    win.searchIcon.setStyleSheet("QPushButton::hover {padding-left: 1px; padding-top: 1px}")

    win.timerBox = TimerBox(win)
    win.timerBox.setFont(win.minecraftFont)
    win.timerBox.setText("0:00:00")
    win.timerBox.setEnabled(False)
    win.timerBox.adjustSize()

    win.timerIcon = TimerIcon(QIcon(win.getIconPath("hourglass-start")), "", win)
    win.timerIcon.setIconSize(QSize(14, 14))
    win.timerIcon.setStyleSheet("QPushButton::hover {padding-left: 1px; padding-top: 1px}")

    win.deliveryBox = QLineEdit(win)
    win.deliveryBox.setEnabled(False)

    win.deliverybutton = QPushButton(win)
    win.deliverybutton.setToolTip('Daily Delivery')
    win.deliverybutton.setIconSize(QSize(12, 12))
    win.deliverybutton.clicked.connect(lambda: openRewards(win))


    # TODO: Add the profile button and menu

    #win.profileBox = QLineEdit(win)
    #win.profileBox.setEnabled(False)

    #win.profilebutton = QPushButton(win)
    #win.profilebutton.setToolTip('Profile')
    #win.profilebutton.setIconSize(QSize(14, 14))
    #win.profilebutton.clicked.connect(win.openProfile)
    
    win.table = Table(win)

    win.minimizebutton = QPushButton(win)
    win.minimizebutton.setToolTip('Minimize')
    win.minimizebutton.setIconSize(QSize(20, 20))
    win.minimizebutton.clicked.connect(win.mini)

    win.maximizebutton = QPushButton(win)
    win.maximizebutton.setToolTip('Maximize')
    win.maximizebutton.setIconSize(QSize(20, 20))
    win.maximizebutton.clicked.connect(win.maxi)

    win.exitbutton = QPushButton(win)
    win.exitbutton.setToolTip('Quit Overlay')
    win.exitbutton.setIconSize(QSize(30, 30))
    win.exitbutton.clicked.connect(win.close)


def updateComponents(win) -> None:
    """
    Update the components of the overlay
    
    :param win: The Overlay window
    """
    win.menuButton.setStyleSheet(win.themeStyle.buttonsStyle)
    win.menuButton.update()

    win.overlayTitle.setStyleSheet(win.themeStyle.titleStyle)
    win.overlayTitle.update()

    win.searchIcon.setIcon(QIcon(win.getIconPath("search")))
    win.searchIcon.update()

    win.searchBox.setStyleSheet(win.themeStyle.searchBarStyle)
    win.searchBox.update()

    win.timerIcon.setIcon(QIcon(win.getIconPath("hourglass-start")))
    win.timerIcon.update()

    win.timerBox.setStyleSheet(win.themeStyle.timerBarStyle)
    win.timerBox.update()

    win.deliverybutton.setStyleSheet(win.themeStyle.buttonsStyle)
    win.deliverybutton.setIcon(QIcon(win.getIconPath("gift")))
    win.deliverybutton.update()

    win.deliveryBox.setStyleSheet(win.themeStyle.timerBarStyle)
    win.deliveryBox.update()

    #win.profilebutton.setStyleSheet(win.themeStyle.buttonsStyle)
    #win.profilebutton.setIcon(QIcon(win.getIconPath("user")))
    #win.profilebutton.update()

    #win.profileBox.setStyleSheet(win.themeStyle.timerBarStyle)
    #win.profileBox.update()
    
    win.table.setStyleSheet(win.themeStyle.tableStyle)
    win.table.VscrollBar.setStyleSheet(win.themeStyle.VscrollBarStyle)
    win.table.HscrollBar.setStyleSheet(win.themeStyle.HscrollBarStyle)

    for i in range(0, win.table.rowCount()):
        for j in range(0, win.table.columnCount()):
            item = win.table.cellWidget(i, j)
            if type(item) == QPushButton and item.property("name") == "dots":
                item.setIcon(QIcon(win.getIconPath("dots")))
        
    win.table.update()

    win.minimizebutton.setStyleSheet(win.themeStyle.buttonsStyle)
    win.minimizebutton.setIcon(QIcon(win.getIconPath("minimize")))
    win.minimizebutton.update()

    win.maximizebutton.setStyleSheet(win.themeStyle.buttonsStyle)
    win.maximizebutton.setIcon(QIcon(win.getIconPath("maximize")))
    win.maximizebutton.update()

    win.exitbutton.setStyleSheet(win.themeStyle.closeButtonStyle)
    win.exitbutton.setIcon(QIcon(win.getIconPath("close")))
    win.exitbutton.update()

    if win.themeStyle.icon == "custom":
        count = 0
        for theme in win.themes:
            if theme[0] == win.configTheme:
                idx = count
            count += 1

        if win.themes[idx][1] != "":
            win.menuButton.setIcon(QIcon(win.themes[idx][1]))
        else:
            win.menuButton.setIcon(QIcon(f"{win.pathAssets}/polsu/Polsu__.png"))
    else:
        win.menuButton.setIcon(QIcon(f"{win.pathAssets}/polsu/Polsu__.png"))
    win.menuButton.update()

    win.overlayTitle.setText(win.themeStyle.name)
    win.overlayTitle.update()

    win.update()


def updateGeometry(win) -> None:
    """
    Update the components of the overlay
    """
    win.searchIcon.setGeometry(263, 10, 19, 19)
    win.searchBox.setGeometry(260, 8, 170, 23)
    win.timerIcon.setGeometry(443, 10, 19, 19)
    win.timerBox.setGeometry(440, 8, 90, 23)
    win.deliverybutton.setGeometry(541, 9, 20, 20)
    win.deliveryBox.setGeometry(540, 8, 22, 22)
    #win.profilebutton.setGeometry(571, 9, 20, 20)
    #win.profileBox.setGeometry(570, 8, 22, 22)
    win.table.setGeometry(5, 45, win.size().width()-10, win.size().height()-50)
    win.minimizebutton.setGeometry(win.size().width() - 94, 4, 30, 30)
    win.maximizebutton.setGeometry(win.size().width() - 64, 4, 30, 30)
    win.exitbutton.setGeometry(win.size().width() - 34, 4, 30, 30)

    if win.height() >= 220:
        win.deliverybutton.setEnabled(True)
    else:
        win.deliverybutton.setEnabled(False)


    if win._rewardsOpened:
        openRewards(win)
        
        if win.height() >= 220:
            openRewards(win)

    if win._menuOpened:
        win.open_menu()
        win.open_menu()

        win.menu.close_menu.setGeometry(win.POPUPWIDTH, 2, win.width(), win.height())

        if win._settingsMenuOpened:
            if win.width() < win.POPUPWIDTH+430 or win.height() < win.POPUPWIDTH+70:
                win.menu.close_settingsMenu()
            else:
                win.menu.settingsMenu.setGeometry(win.POPUPWIDTH, 34, win.width(), win.height())
        if win._infoMenuOpened:
            if win.width() < win.POPUPWIDTH+430 or win.height() < win.POPUPWIDTH+70:
                win.menu.close_infoMenu()
            else:
                win.menu.infoMenu.setGeometry(win.POPUPWIDTH, 34, win.width(), win.height())
    
    if win._apiKeyMenuOpened:
        win.close_apikey_menu()

        openSettings(win)


def enterPress(win) -> None:
    """
    When the user press enter in the search box
    
    :param win: The Overlay window
    """
    win.searchBox.setDisabled(True)

    av = False
    for row in range(win.table.rowCount()):
        _item = win.table.item(row, 2)
        
        if _item and _item.value.lower() == win.searchBox.text().lower():
            win.table.selectRow(0)
            win.table.selectRow(row)

            for i in range(0, win.table.columnCount()):
                __item = win.table.item(row, i)
                __item.setData(Qt.UserRole, 2)

                anim = QVariantAnimation(
                    win,
                    duration=400,
                    startValue=QColor("transparent"),
                    endValue=QColor(win.themeStyle.table_highlight)
                )
                anim.valueChanged.connect(partial(setColor, __item))
                anim.start(QAbstractAnimation.DeleteWhenStopped)

            av = True

    if not av:
        win.player.getPlayer([win.searchBox.text()], True)

    win.searchBox.setText("")
    win.searchBox.setDisabled(False)
