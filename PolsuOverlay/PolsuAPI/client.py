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
from .requests import Polsu as PolReq
from .objects.key import APIKey
from .objects.player import Player as Pl
from .exception import APIError


import asyncio

from async_timeout import timeout


timeout_time = 60


def Polsu(key: str):
    """
    Create an instance of PolsuClient

    :param key: Polsu API Key
    :return: Instance of PolsuClient
    """
    return PolsuClient(key)


class PolsuClient:
    """
    A class representing the Polsu Client
    """
    def __init__(self, key: str) -> None:
        self.client = PolReq(key)
        self.api_key = key
        
        self.key = Key(self.client)
        self.player = Player(self.client)


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

