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
┃                               © 2023 - 2024, Polsu Development - All rights reserved                                 ┃
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
from .api import Polsu as PolReq
from .objects.key import APIKey
from .objects.player import Player as Pl
from .objects.user import User
from .exception import APIError


import asyncio

from async_timeout import timeout


timeout_time = 60


class Polsu:
    """
    A class representing the Polsu Client
    """
    def __init__(self, key: str, logger) -> None:
        self.client = PolReq(key, logger)
        
        self.key = Key(self.client)
        self.user = User(self.client)
        self.player = Player(self.client)


    def updateKey(self, key: str) -> None:
        """
        Update the API Key

        :param key: The new API Key
        """
        self.client.key = key


class Key:
    """
    A class representing a Polsu API Key
    """
    def __init__(self, client: PolReq) -> None:
        self.client = client
        

    async def get(self) -> APIKey:
        """
        Check if the API Key is valid and get the API Key stats

        :return: An instance of APIKey, representing the Polsu API Key
        """
        try:
            async with timeout(timeout_time):
                return await self.client.get_key_stats()
        except asyncio.TimeoutError:
            raise APIError


class User:
    """
    A class representing a Polsu Overlay User
    """
    def __init__(self, client: PolReq) -> None:
        self.client = client
        

    async def login(self) -> User:
        """
        Login to the Polsu API

        :return: An instance of User, representing the Polsu Overlay User
        """
        try:
            async with timeout(timeout_time):
                return await self.client.login()
        except asyncio.TimeoutError:
            raise APIError


    async def logout(self, timestamp: int) -> None:
        """
        Logout of the Overlay

        :param timestamp: The timestamp of the overlay launch
        """
        try:
            async with timeout(timeout_time):
                return await self.client.logout(timestamp)
        except asyncio.TimeoutError:
            raise APIError


class Player:
    """
    A class representing a Hypixel Player
    """
    def __init__(self, client: PolReq) -> None:
        self.client = client
        

    async def get(self, player: str) -> Pl:
        """
        Get a Player stats

        :param player: A Player (uuid or username)
        :return: An instance of Pl, representing the Player stats
        """
        try:
            async with timeout(timeout_time):
                return await self.client.get_stats(player)
        except asyncio.TimeoutError:
            raise APIError


    async def post(self, players: str) -> list[Pl]:
        """
        Get a Player stats

        :param players: A list of Players (uuid or username)
        :return: An list of instances of Pl, representing the Player stats
        """
        try:
            async with timeout(timeout_time):
                return await self.client.post_stats(players)
        except asyncio.TimeoutError:
            raise APIError
        

    async def loadQuickbuy(self, uuid: str) -> None:
        """
        Load the Player quickbuy

        :param uuid: The Player UUID
        """
        try:
            async with timeout(timeout_time):
                return await self.client.load_quickbuy(uuid)
        except asyncio.TimeoutError:
            raise APIError


    async def loadSkin(self, player: Pl) -> None:
        """
        Load the Player skin

        :param player: The Player
        """
        try:
            async with timeout(timeout_time):
                return await self.client.load_skin(player)
        except asyncio.TimeoutError:
            raise APIError
