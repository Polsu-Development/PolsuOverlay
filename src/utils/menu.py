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
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath


def menuPaintEvent(parent, opacity: float = 0.8) -> None:
    """
    Paint the menu
    
    :param parent: The parent of the menu
    :param opacity: The opacity of the menu
    """
    x = -1
    y = 2
    width = parent.size().width() - parent.win.POPUPWIDTH
    height = parent.size().height() - 34
    
    painter = QPainter(parent)
    painter.setPen(QPen(QColor(parent.win.themeStyle.color), 1))
    painter.setBrush(QColor(parent.win.themeStyle.color))
    painter.setOpacity(opacity)


    # Menu
    path = QPainterPath()
    path.moveTo(x, y)
    path.lineTo(x, height)
    path.lineTo(width - 2 * parent.win._cornerRadius, height)
    path.arcTo(width - 2 * parent.win._cornerRadius, y + (height - 2 * parent.win._cornerRadius), 2 * parent.win._cornerRadius, 2 * parent.win._cornerRadius, 270.0, 90.0)
    path.lineTo(width, y)
    painter.setRenderHints(QPainter.Antialiasing)
    painter.drawPath(path)


    painter.setBrush(QColor("#5b5f62"))
    painter.setOpacity(0.8)
    painter.drawRoundedRect(10, 10, 420, 267, 20.0, 20.0)

    painter.end()


def leftMenuPaintEvent(parent) -> None:
    """
    Paint the left menu

    :param parent: The parent of the menu
    """
    x = -1
    y = 2
    width = parent.win.POPUPWIDTH
    height = parent.size().height()-36
    
    painter = QPainter(parent)
    painter.setOpacity(0.8)
    painter.setPen(QPen(QColor(parent.win.themeStyle.color), 1))
    painter.setBrush(QColor(parent.win.themeStyle.color))

    # Menu
    path = QPainterPath()
    path.moveTo(x, y)
    path.lineTo(x, y + (height - 2 * parent.win._cornerRadius))
    path.arcTo(x, y + (height - 2 * parent.win._cornerRadius), 2 * parent.win._cornerRadius, 2 * parent.win._cornerRadius, 180.0, 90.0)
    path.lineTo(width, y + height)
    path.lineTo(width, y)
    path.lineTo(x + parent.win._cornerRadius, y)
    painter.drawPath(path)

    painter.end()
