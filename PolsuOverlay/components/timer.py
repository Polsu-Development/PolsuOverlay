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
from PyQt5.QtWidgets import QLineEdit, QToolTip, QPushButton
from PyQt5 import QtCore


from datetime import timedelta


class TimerBox(QLineEdit):
    def __init__(self, parent):
        QLineEdit.__init__(self, parent=parent)
        self.win = parent
        
        self._last_event_pos = None

    def event(self,event):
        if event.type() == QtCore.QEvent.ToolTip:
            self._last_event_pos = event.globalPos()
            return True
        elif event.type() == QtCore.QEvent.Leave:
            self._last_event_pos = None
            QToolTip.hideText()
        return QLineEdit.event(self,event)

    def updateToolTip(self):
        if self._last_event_pos:
            QToolTip.hideText()
            QToolTip.showText(self._last_event_pos, f"Total Time: {timedelta(seconds=self.win.overlayTimer)}")


class TimerIcon(QPushButton):
    def __init__(self, icon, text, parent):
        QPushButton.__init__(self, icon=icon, text=text, parent=parent)
        self.win = parent
        
        self._last_event_pos = None

    def event(self,event):
        if event.type() == QtCore.QEvent.ToolTip:
            self._last_event_pos = event.globalPos()
            return True
        elif event.type() == QtCore.QEvent.Leave:
            self._last_event_pos = None
            QToolTip.hideText()
        return QPushButton.event(self,event)

    def updateToolTip(self):
        if self._last_event_pos:
            QToolTip.hideText()
            QToolTip.showText(self._last_event_pos, f"Total Time: {timedelta(seconds=self.win.overlayTimer)}")