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
from ..utils.text import text2html
from ..utils.skin import SkinIcon
from ..utils.quickbuy import QuickbuyImage
from ..utils.sorting import TableSortingItem
from ..utils.ping import getPingColour

from ..PolsuAPI.objects.player import Player


from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView, QScrollBar, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QIcon, QColor, QFont

import re
import traceback

from typing import Literal


class Table(QTableWidget):
    """
    A class representing a table
    """
    def __init__(self, window) -> None:
        """
        Initialise the Table class
        
        :param window: The window
        """
        super(Table, self).__init__(window)
        self.win = window

        # Header aka Columns title
        self.header=['⠀', '˅ 0', 'Player⠀⠀⠀⠀⠀⠀ ', 'TAG', 'WS', 'FKDR', 'Finals', 'WLR', ' Wins', 'BBLR', 'Beds', 'Requeue', 'Ping', '⠀', '⠀', '⠀']

        # Settings
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setShowGrid(False)

        # Font stuff
        self.setFont(self.win.getFont())
        self.horizontalHeader().setFont(self.win.getFont())

        # Need to change the style here, before we set the number of columns or the header doesn't update.
        self.setStyleSheet(self.win.themeStyle.tableStyle)
        
        # Number of columns
        self.setColumnCount(len(self.header))

        # Scroll Bar
        self.VscrollBar = QScrollBar(self)
        self.setVerticalScrollBar(self.VscrollBar)
        self.HscrollBar = QScrollBar(self)
        self.setHorizontalScrollBar(self.HscrollBar)

        # Sorting
        self.setSortingEnabled(True)
        self.sortByColumn(self.win.configSorting[0], self.win.configSorting[1])
        
        # Header
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionsMovable(True)
        self.horizontalHeader().setVisible(True)
        self.horizontalHeader().sortIndicatorChanged.connect(self.sort)
        self.setHorizontalHeaderLabels(self.header)

        self.verticalHeader().hide()


        # Columns Width
        self.horizontalHeader().setMinimumSectionSize(30)

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.horizontalHeader().resizeSection(0, 30)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().resizeSection(2, 220)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(9, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(11, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(12, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(13, QHeaderView.Fixed)
        self.horizontalHeader().resizeSection(13, 25)
        self.horizontalHeader().setSectionResizeMode(14, QHeaderView.Fixed)
        self.horizontalHeader().resizeSection(14, 25)
        self.horizontalHeader().setSectionResizeMode(15, QHeaderView.Fixed)
        self.horizontalHeader().resizeSection(15, 25)

        self.verticalHeader().setDefaultSectionSize(round((16 * QFontMetrics(self.win.getFont()).height()) / 100))

        self.count = -1

        self.skin = SkinIcon(self.win, self)
        self.quickbuy = QuickbuyImage(self.win)


    def insert(self, player: Player) -> None:
        """
        Insert a player in the table
        
        :param player: The player to insert
        """
        self.win.logger.info(f"Inserting {player.username} ({player.uuid}) in the table.")

        try:
            # We need to disable the sorting before inserting or some data will be hidden...
            self.setSortingEnabled(False)

            self.count += 1
            self.insertRow(self.count)

            if player.bedwars.winstreak == -1:
                ws = "§7-"
            else:
                ws = f"§f{player.bedwars.winstreak:,d}"

            label = QLabel(text2html(player.bedwars.formatted + " "), self)
            label.setFont(self.win.minecraftFont)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.setCellWidget(self.count, 1, label)
            label.setProperty("name", "mcfont")
            self.setItem(self.count, 1, TableSortingItem(player.bedwars.stars))

            pattern = re.compile(r"(?:§.\[.*?\] )?(\w+)(?: (?P<suffix>.*))?")

            # Search for the pattern in player.rank
            match = pattern.search(player.rank)
        

            # Get the prefix and suffix from the match
            if match.group('suffix'):
                playername = player.rank[:match.start('suffix')].strip()
                suffix = match.group('suffix')
            else:
                playername = player.rank.strip()
                suffix = ' '

            # Create the playername label with minecraftFont
            playername = QLabel(text2html(playername), self)
            playername.setFont(self.win.minecraftFont)
            playername.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
            # Create the suffix label with NotoEmoji font
            suffix_label = QLabel(suffix, self)
            suffix_label.setFont(QFont("NotoEmoji", 11))
            suffix_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            # Create a layout and add the labels to it
            layout = QHBoxLayout()
            layout.addWidget(playername)
            layout.addWidget(suffix_label)
            layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

            # Create a widget, set its layout, and set it as the cell widget
            widget = QWidget(self)
            widget.setLayout(layout)
            self.setCellWidget(self.count, 2, widget)
            self.setItem(self.count, 2, TableSortingItem(player.username))

            label = QLabel(text2html(player.tag + " "), self)
            label.setFont(self.win.getFont())
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCellWidget(self.count, 3, label)
            self.setItem(self.count, 3, TableSortingItem(re.sub(r"(?i)�[0-9A-FK-OR]", "", player.tag)))

            label = QLabel(text2html(f"{ws} "), self)
            label.setFont(self.win.getFont())
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCellWidget(self.count, 4, label)
            self.setItem(self.count, 4, TableSortingItem(player.bedwars.winstreak))

            label = QLabel(text2html(f"{player.bedwars.fkdr} ", colour=player.bedwars.requeue.colour), self)
            label.setFont(self.win.getFont())
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCellWidget(self.count, 5, label)
            self.setItem(self.count, 5, TableSortingItem(player.bedwars.fkdr))

            label = QLabel(text2html(f"{player.bedwars.fkills:,d} ", colour=player.bedwars.requeue.colour), self)
            label.setFont(self.win.getFont())
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCellWidget(self.count, 6, label)
            self.setItem(self.count, 6, TableSortingItem(player.bedwars.fkills))

            label = QLabel(text2html(f"{player.bedwars.wlr} ", colour=player.bedwars.requeue.colour), self)
            label.setFont(self.win.getFont())
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCellWidget(self.count, 7, label)
            self.setItem(self.count, 7, TableSortingItem(player.bedwars.wlr))

            label = QLabel(text2html(f"{player.bedwars.wins:,d} ", colour=player.bedwars.requeue.colour), self)
            label.setFont(self.win.getFont())
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCellWidget(self.count, 8, label)
            self.setItem(self.count, 8, TableSortingItem(player.bedwars.wins))
            
            label = QLabel(text2html(f"{player.bedwars.bblr} ", colour=player.bedwars.requeue.colour), self)
            label.setFont(self.win.getFont())
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCellWidget(self.count, 9, label)
            self.setItem(self.count, 9, TableSortingItem(player.bedwars.bblr))

            label = QLabel(text2html(f"{player.bedwars.broken:,d} ", colour=player.bedwars.requeue.colour), self)
            label.setFont(self.win.getFont())
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCellWidget(self.count, 10, label)
            self.setItem(self.count, 10, TableSortingItem(player.bedwars.broken))

            if player.nicked:
                label = QLabel(text2html(f"§7- "), self)
            else:
                label = QLabel(text2html(f"{player.bedwars.requeue.index} ", colour=player.bedwars.requeue.colour), self)

            label.setFont(self.win.getFont())
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCellWidget(self.count, 11, label)
            self.setItem(self.count, 11, TableSortingItem(player.bedwars.requeue.raw))

            if player.ping.ping == 0:
                label = QLabel(text2html(f"§7-"), self)
            else:
                label = QLabel(text2html(f"{getPingColour(player.ping.ping)}{player.ping.ping:,d}ms "), self)
            label.setFont(self.win.getFont())
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCellWidget(self.count, 12, label)
            self.setItem(self.count, 12, TableSortingItem(player.ping.ping))

            #button = QPushButton(self)
            #button.setIcon(QIcon(self.win.getIconPath("dots")))
            #button.setStyleSheet(self.win.themeStyle.buttonsStyle)
            #button.clicked.connect(None)
            #button.setEnabled(False)
            #button.setProperty("name", "dots")
            #self.setCellWidget(self.count, 12, button)
            #self.setItem(self.count, 12, TableSortingItem(self.count))

            button = QPushButton(self)
            button.setIcon(QIcon(self.win.getIconPath("remove")))
            button.setStyleSheet(self.win.themeStyle.buttonsStyle)
            button.clicked.connect(lambda: self.removePlayerFromUUID(player.uuid))
            button.setProperty("name", "remove")
            self.setCellWidget(self.count, 13, button)
            self.setItem(self.count, 13, TableSortingItem(player.uuid))


            plugin_bl = False
            if player.blacklisted.status:
                if self.win.plugins.askPlugins("global_blacklist"):
                    plugin_bl = True
                else:
                    button = QPushButton(self)
                    button.setIcon(QIcon(self.win.getIconPath("global-blacklist")))
                    button.setToolTip(f"<b>Polsu Blacklisted</b><br><br><b>Reason:</b><br>{player.blacklisted.reason}")
                    button.setProperty("name", "global-blacklist")
                    self.setCellWidget(self.count, 14, button)
                    self.setItem(self.count, 14, TableSortingItem(1))
            else:
                button = QPushButton(self)
                self.setCellWidget(self.count, 14, button)
                self.setItem(self.count, 14, TableSortingItem(0))


            # Load the local blacklist
            if not player.local:
                player.local = self.win.blacklist.findPlayer(player)


            if player.local.status:
                button = QPushButton(self)
                button.setIcon(QIcon(self.win.getIconPath("blacklist")))
                button.setToolTip(f"<b>Local Blacklisted</b><br><br><b>Reason:</b><br>{player.local.reason}<br><br><b>Blacklist:</b><br>{player.local.blacklist}")
                button.setProperty("name", "blacklist")
                self.setCellWidget(self.count, 15, button)
                self.setItem(self.count, 15, TableSortingItem(1))
            else:
                button = QPushButton(self)
                self.setCellWidget(self.count, 15, button)
                self.setItem(self.count, 15, TableSortingItem(0))


            self.skin.loadSkin(player, self.count)


            if player.blacklisted.status and self.win.configGlobalBlacklist and not plugin_bl or player.local.status:
                color = QColor("#FF0000")
                color.setAlpha(50)
                for j in range(self.columnCount()):
                    item = self.item(self.count, j)
                    if item:
                        item.setBackground(color)


            # Done - Enable sorting again
            self.setSortingEnabled(True)

            self.updateHeaders()

            self.win.plugins.broadcast("on_player_insert", player)
        except:
            self.win.logger.critical(f"An error occurred while inserting {player.username} ({player.uuid}) in the table!\n\nTraceback: {traceback.format_exc()}")


    def getPlayers(self) -> list:
        """
        Get the players
        
        :return: The players
        """
        players = []

        for row in range(self.rowCount()):
            _item = self.item(row, 2)

            if _item:
                players.append(_item.value)
        
        return players


    def getUUIDs(self) -> list:
        """
        Get the UUIDs
        
        :return: The UUIDs
        """
        uuids = []

        for row in range(self.rowCount()):
            _item = self.item(row, 13)

            if _item:
                uuids.append(_item.value)
        
        return uuids


    def resetTable(self) -> None:
        """
        Reset the table
        """
        self.count = -1

        self.clear()
        self.updateHeaders()
        self.setRowCount(0)
        self.update()


    def removePlayerFromUUID(self, uuid: str) -> None:
        """
        Remove a player from the table
        
        :param uuid: The player's UUID
        """
        for row in range(self.rowCount()):
            _item = self.item(row, 13)

            if _item and _item.value == uuid:
                self.removeRow(row)
                self.count -= 1
                break
        
        self.updateHeaders()
    

    def removePlayerFromName(self, name: str) -> None:
        """
        Remove a player from the table
        
        :param name: The player's name
        """
        for row in range(self.rowCount()):
            _item = self.item(row, 2)

            if _item and _item.value == name:
                self.removeRow(row)
                self.count -= 1
                break
        
        self.updateHeaders()


    def getHeaders(self) -> list:
        """
        Get the headers
        
        :return: The headers
        """
        return self.header


    def updateHeaders(self) -> None:
        """
        Update the headers
        """
        hd = self.header
        hd[1] = f"˅ {self.count+1}"
        self.setHorizontalHeaderLabels(hd)


    def sort(self, column: int, order: int) -> None:
        """
        Handle the sorting
        
        :param column: The column
        :param order: The order
        """
        self.sortByColumn(column, order)

        self.win.settings.update("sorting", [column, order])


    def setGlobalBlacklist(self, uuid: str, tooltip: str, icon: Literal["custom-blacklist", "verified", "annoying", "info"], text: str = "") -> None:
        """
        Set the global blacklist
        
        :param uuid: The player uuid
        :param tooltip: The tooltip
        :param icon: The icon
        :param text: The text
        """
        self.setSortingEnabled(False)

        for row in range(self.rowCount()):
            _item = self.item(row, 13)

            if _item and _item.value == uuid:
                button = QPushButton(self)
                button.setFont(self.win.getFont())
                button.setText(text)
                button.setStyleSheet("""
                QPushButton {
                    color:white;
                }                
                """)

                if icon not in ["custom-blacklist", "verified", "annoying", "info"]:
                    button.setIcon(QIcon(self.win.getIconPath("custom-blacklist")))
                else:
                    button.setIcon(QIcon(self.win.getIconPath(icon)))
                button.setToolTip(tooltip)
                button.setProperty("name", "custom-blacklist")
                self.setCellWidget(row, 14, button)
                self.setItem(row, 14, TableSortingItem(0))

        self.setSortingEnabled(True)


    def setLineColour(self, uuid: str, colour: str = "FF0000") -> None:
        """
        Set the blacklisted line
        
        :param uuid: The player uuid
        :param colour: The colour
        """
        self.setSortingEnabled(False)

        for row in range(self.rowCount()):
            _item = self.item(row, 13)

            if _item and _item.value == uuid:
                color = QColor(colour)
                color.setAlpha(50)
                for j in range(self.columnCount()):
                    item = self.item(row, j)
                    if item:
                        item.setBackground(color)

        self.setSortingEnabled(True)
