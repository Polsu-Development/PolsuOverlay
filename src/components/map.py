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
from ..utils.menu import leftMenuPaintEvent


from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal, QObject, QSize
from PyQt5.QtGui import QIcon

import asyncio


def openMap(win) -> None:
    """
    Open the Map window
    
    :param win: The Overlay window
    """
    if not win._apiKeyMenuOpened:
        if win._menuOpened:
            win.open_menu()

        if not win._rewardsOpened:
            win.searchBox.setEnabled(False)
            win.searchIcon.setEnabled(False)

            win.rewards = Map(win)
            win.rewards.move(0, 34)
            win.rewards.resize(win.width(), win.height())
            win.rewards.SIGNALS.CLOSE.connect(lambda: closeMap(win))
            win._rewardsOpened = True
            win.rewards.show()
        else:
            closeMap(win)
    

def closeMap(win) -> None:
    """
    Close the rewards window
    
    :param win: The Overlay window
    """
    win.rewards.close()
    win._rewardsOpened = False

    win.searchBox.setEnabled(True)
    win.searchIcon.setEnabled(True)
    win.setMinimumSize(680, 150)


class WidgetSignals(QObject):
    """
    WidgetSignals is a class that contains all the signals of the Rewards widget
    """
    CLOSE = pyqtSignal()


class Map(QWidget):
    """
    Map is a QWidget that contains all the map information
    """
    def __init__(self, window) -> None:
        """
        Initialise the Map widget
        
        :param window: The Overlay window
        """
        super(Map, self).__init__(window)
        self.win = window
        

        self.close_menu = QPushButton("", self)
        self.close_menu.setGeometry(self.win.POPUPWIDTH, 2, self.win.width(), self.win.height())
        self.close_menu.clicked.connect(self._onclose)


        self.firstRewardTextTitle = QLabel("", self)
        self.firstRewardTextTitle.setFont(self.win.getFont())
        self.firstRewardTextTitle.adjustSize()
        self.firstRewardTextTitle.setStyleSheet(self.win.themeStyle.deliveryTextTitleStyle)
        self.firstRewardTextTitle.setGeometry(15, 2, 220, 40)

        self.firstRewardTextSmall = QLabel("", self)
        self.firstRewardTextSmall.setFont(self.win.getFont())
        self.firstRewardTextSmall.adjustSize()
        self.firstRewardTextSmall.setStyleSheet(self.win.themeStyle.deliveryTextSmallStyle)
        self.firstRewardTextSmall.setGeometry(15, 20, 220, 40)

        self.firstRewardButton = QPushButton(self)
        self.firstRewardButton.setIcon(QIcon(self.win.getIconPath("1")))
        self.firstRewardButton.setToolTip('First Reward')
        self.firstRewardButton.setIconSize(QSize(24, 24))
        self.firstRewardButton.setStyleSheet(self.win.themeStyle.deliveryButtonsStyle)
        self.firstRewardButton.setGeometry(15, 12, 220, 40)
        self.firstRewardButton.clicked.connect(lambda: self.claim(0))

        self.firstRewardIcon = QPushButton(self)
        self.firstRewardIcon.setToolTip('Rarity')
        self.firstRewardIcon.setIconSize(QSize(15, 15))
        self.firstRewardIcon.setStyleSheet("QPushButton::hover {padding-left: 1px; padding-top: 1px}")
        self.firstRewardIcon.setGeometry(215, 22, 20, 20)


        self.secondRewardTextTitle = QLabel("", self)
        self.secondRewardTextTitle.setFont(self.win.getFont())
        self.secondRewardTextTitle.adjustSize()
        self.secondRewardTextTitle.setStyleSheet(self.win.themeStyle.deliveryTextTitleStyle)
        self.secondRewardTextTitle.setGeometry(15, 47, 220, 40)

        self.secondRewardTextSmall = QLabel("", self)
        self.secondRewardTextSmall.setFont(self.win.getFont())
        self.secondRewardTextSmall.adjustSize()
        self.secondRewardTextSmall.setStyleSheet(self.win.themeStyle.deliveryTextSmallStyle)
        self.secondRewardTextSmall.setGeometry(15, 65, 220, 40)

        self.secondRewardButton = QPushButton(self)
        self.secondRewardButton.setIcon(QIcon(self.win.getIconPath("2")))
        self.secondRewardButton.setToolTip('Second Reward')
        self.secondRewardButton.setIconSize(QSize(24, 24))
        self.secondRewardButton.setStyleSheet(self.win.themeStyle.deliveryButtonsStyle)
        self.secondRewardButton.setGeometry(15, 57, 220, 40)
        self.secondRewardButton.clicked.connect(lambda: self.claim(1))

        self.secondRewardIcon = QPushButton(self)
        self.secondRewardIcon.setToolTip('Rarity')
        self.secondRewardIcon.setIconSize(QSize(15, 15))
        self.secondRewardIcon.setStyleSheet("QPushButton::hover {padding-left: 1px; padding-top: 1px}")
        self.secondRewardIcon.setGeometry(215, 67, 20, 20)


        self.thirdRewardTextTitle = QLabel("", self)
        self.thirdRewardTextTitle.setFont(self.win.getFont())
        self.thirdRewardTextTitle.adjustSize()
        self.thirdRewardTextTitle.setStyleSheet(self.win.themeStyle.deliveryTextTitleStyle)
        self.thirdRewardTextTitle.setGeometry(15, 92, 220, 40)

        self.thirdRewardTextSmall = QLabel("", self)
        self.thirdRewardTextSmall.setFont(self.win.getFont())
        self.thirdRewardTextSmall.adjustSize()
        self.thirdRewardTextSmall.setStyleSheet(self.win.themeStyle.deliveryTextSmallStyle)
        self.thirdRewardTextSmall.setGeometry(15, 110, 220, 40)

        self.thirdRewardButton = QPushButton(self)
        self.thirdRewardButton.setIcon(QIcon(self.win.getIconPath("3")))
        self.thirdRewardButton.setToolTip('Third Reward')
        self.thirdRewardButton.setIconSize(QSize(24, 24))
        self.thirdRewardButton.setStyleSheet(self.win.themeStyle.deliveryButtonsStyle)
        self.thirdRewardButton.setGeometry(15, 102, 220, 40)
        self.thirdRewardButton.clicked.connect(lambda: self.claim(2))

        self.thirdRewardIcon = QPushButton(self)
        self.thirdRewardIcon.setToolTip('Rarity')
        self.thirdRewardIcon.setIconSize(QSize(15, 15))
        self.thirdRewardIcon.setStyleSheet("QPushButton::hover {padding-left: 1px; padding-top: 1px}")
        self.thirdRewardIcon.setGeometry(215, 112, 20, 20)


        title = QLabel("Daily Delivery", self)
        title.setStyleSheet(self.win.themeStyle.sideBarTextStyle)
        title.adjustSize()
        title.setFont(self.win.getFont())
        title.move(5, self.win.size().height()-70)

        self.SIGNALS = WidgetSignals()

        if self.win.reward:
            self.updateWindow()

            self.firstRewardButton.setEnabled(True)
            self.secondRewardButton.setEnabled(True)
            self.thirdRewardButton.setEnabled(True)
        else:
            self.firstRewardButton.setEnabled(False)
            self.secondRewardButton.setEnabled(False)
            self.thirdRewardButton.setEnabled(False)
        

    def paintEvent(self, event) -> None:
        """
        Paint the background
        """
        return leftMenuPaintEvent(self)

    
    def _onclose(self) -> None:
        """
        Emit the close signal
        """
        self.SIGNALS.CLOSE.emit()
