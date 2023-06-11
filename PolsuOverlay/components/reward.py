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
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal, QObject, QSize
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QPainterPath

import asyncio


class WidgetSignals(QObject):
    CLOSE = pyqtSignal()


class Rewards(QWidget):
    def __init__(self, window):
        super(Rewards, self).__init__(window)
        self.win = window
        

        self.close_menu = QPushButton("", self)
        self.close_menu.setGeometry(self.win.POPUPWIDTH, 2, self.win.width(), self.win.height())
        self.close_menu.clicked.connect(self._onclose)


        self.firstRewardTextTitle = QLabel("", self)
        self.firstRewardTextTitle.setFont(self.win.minecraftFont)
        self.firstRewardTextTitle.adjustSize()
        self.firstRewardTextTitle.setStyleSheet(self.win.themeStyle.deliveryTextTitleStyle)
        self.firstRewardTextTitle.setGeometry(15, 2, 220, 40)

        self.firstRewardTextSmall = QLabel("", self)
        self.firstRewardTextSmall.setFont(self.win.minecraftFont)
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
        self.secondRewardTextTitle.setFont(self.win.minecraftFont)
        self.secondRewardTextTitle.adjustSize()
        self.secondRewardTextTitle.setStyleSheet(self.win.themeStyle.deliveryTextTitleStyle)
        self.secondRewardTextTitle.setGeometry(15, 47, 220, 40)

        self.secondRewardTextSmall = QLabel("", self)
        self.secondRewardTextSmall.setFont(self.win.minecraftFont)
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
        self.thirdRewardTextTitle.setFont(self.win.minecraftFont)
        self.thirdRewardTextTitle.adjustSize()
        self.thirdRewardTextTitle.setStyleSheet(self.win.themeStyle.deliveryTextTitleStyle)
        self.thirdRewardTextTitle.setGeometry(15, 92, 220, 40)

        self.thirdRewardTextSmall = QLabel("", self)
        self.thirdRewardTextSmall.setFont(self.win.minecraftFont)
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
        title.setFont(self.win.minecraftFont)
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


    def claim(self, id):
        if self.win.reward:
            asyncio.run(self.win.reward.claim(id))
            self.win.closeRewards()
            title = self.win.reward.rewards[0].title()
            self.win.notif.send(
                title="Hypixel Daily Delivery Reward",
                message=f"Successfully claimed: {title}{' - ' if title != '' else ''}{self.win.reward.rewards[0].small()}"
            )
            self.win.reward = None
    

    def updateWindow(self):
        self.firstRewardButton.setEnabled(True)
        self.secondRewardButton.setEnabled(True)
        self.thirdRewardButton.setEnabled(True)

        self.firstRewardTextTitle.setText(self.win.reward.rewards[0].title())
        self.firstRewardTextSmall.setText(self.win.reward.rewards[0].small())
        self.firstRewardIcon.setIcon(QIcon(self.win.getIconPath(self.win.reward.rewards[0].rarity.lower())))
        self.firstRewardIcon.setToolTip(self.win.reward.rewards[0].rarity)
        self.firstRewardTextTitle.update()
        self.firstRewardTextSmall.update()
        self.firstRewardIcon.update()

        self.secondRewardTextTitle.setText(self.win.reward.rewards[1].title())
        self.secondRewardTextSmall.setText(self.win.reward.rewards[1].small())
        self.secondRewardIcon.setIcon(QIcon(self.win.getIconPath(self.win.reward.rewards[1].rarity.lower())))
        self.secondRewardIcon.setToolTip(self.win.reward.rewards[1].rarity)
        self.secondRewardTextTitle.update()
        self.secondRewardTextSmall.update()
        self.secondRewardIcon.update()

        self.thirdRewardTextTitle.setText(self.win.reward.rewards[2].title())
        self.thirdRewardTextSmall.setText(self.win.reward.rewards[2].small())
        self.thirdRewardIcon.setIcon(QIcon(self.win.getIconPath(self.win.reward.rewards[2].rarity.lower())))
        self.thirdRewardIcon.setToolTip(self.win.reward.rewards[2].rarity)
        self.thirdRewardTextTitle.update()
        self.thirdRewardTextSmall.update()
        self.thirdRewardIcon.update()
        

    def paintEvent(self, event):
        x = -1
        y = 2
        width = self.win.POPUPWIDTH
        height = self.size().height()-36
        
        painter = QPainter(self)
        painter.setOpacity(0.8)
        painter.setPen(QPen(QColor(self.win.themeStyle.color), 1))
        painter.setBrush(QColor(self.win.themeStyle.color))

        # Menu
        path = QPainterPath()
        path.moveTo(x, y)
        path.lineTo(x, y + (height - 2 * self.win._cornerRadius))
        path.arcTo(x, y + (height - 2 * self.win._cornerRadius), 2 * self.win._cornerRadius, 2 * self.win._cornerRadius, 180.0, 90.0)
        path.lineTo(width, y + height)
        path.lineTo(width, y)
        path.lineTo(x + self.win._cornerRadius, y)
        #painter.setRenderHints(QPainter.Antialiasing)
        painter.drawPath(path)

        painter.end()

    
    def _onclose(self):
        self.SIGNALS.CLOSE.emit()
