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
from ..PolsuAPI import Polsu
from ..PolsuAPI.exception import APIError, InvalidAPIKeyError
from ..PolsuAPI.objects.player import Player as Pl

from ..utils.colours import Colours


from PyQt5.QtCore import QThread, pyqtSignal

import asyncio


class Player:
    def __init__(self, win):
        self.win = win

        self.client = Polsu(self.win.configAPIKey)

        self.rqColour = Colours(self.win.configRqColours)


        self.threads = {}
        self.cache = {}

        self.loading = []


    def getPlayer(self, players: list, manual: bool = False):
        for p in players:
            if p != "":
                if p not in self.loading:
                    av = False
                    for row in range(self.win.table.rowCount()):
                        _item = self.win.table.item(row, 2)
                        
                        if _item and _item.value.lower() == p.lower():
                            av = True

                    if not av:
                        try:
                            self.update(self.cache[p], cache=False)
                        except:
                            self.loading.append(p)

                            self.threads[p] = Worker(self.client, p, manual)
                            self.threads[p].playerObject.connect(self.update)
                            self.threads[p].start()


    def update(self, player: Pl, cache: bool = True):
        player.bedwars.requeue.colour = self.rqColour[player.bedwars.requeue.index]

        if player.username in self.loading:
            self.loading.remove(player.username)

        if cache:
            self.cache[player.username] = player

        if player.manual:
            if not player.username in self.win.logs.queue:
                self.win.table.insert(player)
        else:
            self.win.table.insert(player)


    def loadTags(self):
        self.tags = asyncio.run(self.client.tags.get())


class Worker(QThread):
    playerObject = pyqtSignal(object)

    def __init__(self, client, query, manual):
        super(QThread, self).__init__()
        self.client = client
        self.query = query
        self.manual = manual
 

    def run(self):
        try:
            player = asyncio.run(self.client.player.get(self.query))
            player.manual = self.manual
            self.playerObject.emit(player)
        except:
            pass
