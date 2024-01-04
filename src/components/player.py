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
from src import CACHE, DEV_MODE
from ..PolsuAPI import Polsu
from ..PolsuAPI.exception import APIError, InvalidAPIKeyError
from ..PolsuAPI.objects.player import Player as Pl
from ..utils.colours import Colours


import asyncio
import traceback

from PyQt5.QtCore import QThread, pyqtSignal
from time import time
from uuid import uuid4
from typing import Union


class Player:
    """
    The player class, used to get players from the API
    """
    def __init__(self, win) -> None:
        """
        Initialise the class
        
        :param win: The main window
        """
        self.win = win

        self.client = Polsu(self.win.configAPIKey, self.win.logger)

        self.rqColour = Colours(self.win.configRqColours)


        self.threads = {}
        self.cache = {}

        self.loading = []


    def getPlayer(self, players: list, manual: bool = False) -> None:
        """
        Get a player from the API
        
        :param players: The player(s) to get
        :param manual: If the player is manually added
        """
        self.win.logger.debug(f"Loading {len(players)} player{'s' if len(players)>1 else ''}!")
        new = []
        for player in players:
            player = player.split(" ")[0]
            if player == "" or player.startswith("["):
                continue

            cleaned = player.lower()
            if cleaned not in self.loading:
                av = False
                for row in range(self.win.table.rowCount()):
                    _item = self.win.table.item(row, 2)
                    
                    if _item and _item.value.lower() == cleaned:
                        av = True

                if not av:
                    request = False
                    if cleaned in self.cache:
                        if time() - self.cache[cleaned].cached >= CACHE:
                            request = True
                        else:
                            player = self.cache[cleaned]
                            player.manual = manual
                            self.update(player, cache=False)
                    else:
                        request = True

                    if request:
                        self.loading.append(cleaned)

                        new.append(player)

        if len(new) == 1:
            self.win.logger.info(f"Requesting: {new[0]}.")

            try:
                self.threads[cleaned] = Worker(self.client, new[0], manual)
                self.threads[cleaned].playerObject.connect(self.update)
                self.threads[cleaned].start()
            except:
                self.win.logger.error(f"Error while loading a player ({new[0]}).\n\nTraceback: {traceback.format_exc()}")
        else:
            if len(new) > 40:
                nb_slice = 10
            elif len(new) > 20:
                nb_slice = 6
            else:
                nb_slice = 3

            slices = [new[i : i+nb_slice] for i in range(0, len(new), nb_slice)]

            for s in slices:
                self.win.logger.info(f"Requesting: {s}.")

                uuid = str(uuid4())
                while uuid in self.threads:
                    uuid = str(uuid4())

                try:
                    self.threads[uuid] = Worker(self.client, s, manual)
                    self.threads[uuid].playerObject.connect(self.update)
                    self.threads[uuid].start()
                except:
                    self.win.logger.error(f"Error while loading a player slice ({s}).\n\nTraceback: {traceback.format_exc()}")


    def loadPlayer(self, player: str, uuid: str) -> None:
        """
        Load a player from the API
        
        :param player: The player to load
        :param uuid: The player's UUID
        """
        cleaned = player.lower()

        if cleaned not in self.loading:
            self.loading.append(cleaned)

            self.win.logger.info(f"Requesting: {player}. (Connection)")

            try:
                self.threads[cleaned] = Worker(self.client, uuid, True)
                self.threads[cleaned].playerObject.connect(self.setRPCPlayer)
                self.threads[cleaned].start()
            except:
                self.win.logger.error(f"Error while loading a player ({player}) [Manual].\n\nTraceback: {traceback.format_exc()}")


    def setRPCPlayer(self, player: Pl) -> None:
        """
        Set the RPC player

        :param player: The player to set
        """
        if self.win.RPC and player:
            self.win.RPC.setPlayer(player)

        if player:
            self.update(player)


    def update(self, player: Pl, cache: bool = True) -> None:
        """
        Insert a player into the table
        
        :param player: The player to update
        :param cache: If the player should be cached
        """
        if DEV_MODE:
            self.win.logger.debug(f"Updating {player}")

        if isinstance(player, int):
            self.win.logger.warning(f"[{player}] Error while loading a player ({player}).")

            if player == 422:
                self.win.notif.send(
                    title="Error...",
                    message="This player isn't valid!"
                )
            elif player == 404:
                self.win.notif.send(
                    title="Error...",
                    message="This player doesn't exist!"
                )
            elif player == 403:
                self.win.notif.send(
                        title="Error...",
                        message="Something went wrong while loading the player! Is the API Key valid?"
                    )
            elif player == -1:
                self.win.notif.send(
                    title="Error...",
                    message="Malformed player!"
                )
            else:
                self.win.logger.error(f"Error while loading a player.\n\nTraceback: {traceback.format_exc()}")
        elif isinstance(player, InvalidAPIKeyError):
            self.logger.warning(f"[InvalidAPIKeyError] Error while loading a player ({player}).")

            self.win.notif.send(
                title="Error...",
                message="Something went wrong while loading the player! Is the API Key valid?"
            )
        elif player:
            player.bedwars.requeue.colour = self.rqColour[player.bedwars.requeue.index]

            if cache:
                self.cache[player.cleaned] = player

            try:
                if player.manual:
                    self.win.table.insert(player)
                else:
                    if player.username in self.win.logs.queue:
                        self.win.table.insert(player)
            except:
                self.win.logger.error(f"Error while loading a player ({player}).\n\nTraceback: {traceback.format_exc()}")

            if player.cleaned in self.loading:
                self.loading.remove(player.cleaned)
        else:
            self.win.configAPIKey = ""
            self.win.settings.update("APIKey", "")


class Worker(QThread):
    """
    The worker class, used to get players from the API
    """
    playerObject = pyqtSignal(object, str)

    def __init__(self, client, query: Union[list, str], manual: bool = False) -> None:
        """
        Initialise the class
        
        :param client: The Polsu client
        :param query: The query to use
        :param manual: If the player is manually added
        """
        super(QThread, self).__init__()
        self.client = client
        self.query = query
        self.manual = manual
 

    def run(self) -> None:
        """
        Run the thread
        """
        try:
            if isinstance(self.query, list):
                players = asyncio.run(self.client.player.post(self.query))

                if players == None:
                    self.playerObject.emit(False, "")
                else:
                    for player in players:
                        player.manual = self.manual
                        self.playerObject.emit(player, "")
            else:
                player = asyncio.run(self.client.player.get(self.query))

                if player == None:
                    self.playerObject.emit(False, self.query)
                else:
                    player.manual = self.manual
                    self.playerObject.emit(player, self.query)
        except APIError:
            pass
        except InvalidAPIKeyError:
            self.playerObject.emit(None, self.query)
        except:
            self.playerObject.emit(False, self.query)
