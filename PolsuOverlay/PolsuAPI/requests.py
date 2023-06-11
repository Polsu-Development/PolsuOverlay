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
from PolsuOverlay import __header__
from ..utils.path import resource_path

from .objects.key import APIKey
from .objects.player import Player
from .exception import APIError, InvalidAPIKeyError

from aiohttp import ClientSession, ContentTypeError
from json import load


class Polsu:
    """
    A class representing the Polsu API
    """
    def __init__(self, key: str) -> None:
        self.key = key

        # The current API base url
        self.api = "https://api.polsu.xyz"
        
        
    async def get_key_stats(self) -> APIKey:
        """
        Get the Polsu API Key stats

        :return: An instance of APIKey
        """
        try:
            async with ClientSession() as session:
                async with session.get(f"{self.api}/api/key?key={self.key}", headers=__header__) as response:
                    json = await response.json()
                    if not json["success"]:
                        raise InvalidAPIKeyError(self.key)
                    return APIKey(json)
        except ContentTypeError:
            raise APIError
        

    async def get_stats(self, player) -> Player:
        """
        Get a Player Hypixel Stats

        :param player: A player (username or uuid)
        :return: An instance of Player


    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n
    ┃                                                                                                              ┃\n
    ┃                                               >> WARNING <<                                                  ┃\n
    ┃                                                                                                              ┃\n
    ┃  • The following endpoint, '/internal/player' is a private endpoint.                                         ┃\n
    ┃                                                                                                              ┃\n
    ┃  > IT IS STRICTLY FORBIDDEN TO USE IT OUTSIDE POLSU'S OFFICIAL OVERLAY.                                      ┃\n
    ┃  > ANY USAGE OF THIS ENDPOINT FOR OTHER PROJECTS OR FORKS OF POLSU'S OVERLAY ISN'T ALLOWED!                  ┃\n
    ┃                                                                                                              ┃\n
    ┃  • If we notice any suspicious activity on this endpoint, following our Terms of Services, your api key and  ┃\n
    ┃    therefore your account Discord account, will get blacklisted from our Services!                           ┃\n
    ┃  > This means you won't be able to use any of our Services anymore, including Polsu and Polsu's Overlay.     ┃\n
    ┃                                                                                                              ┃\n
    ┃  • Note: This warning applies to all endpoints starting with: '/intenal'                                     ┃\n
    ┃  > You are allowed to use the other endpoints, listed in the documentation at: https://api.polsu.xyz         ┃\n
    ┃                                                                                                              ┃\n
    ┃                                                                                                              ┃\n
    ┃  • If you have any questions, don't hesitate to contact us on discord at: https://discord.polsu.xyz.         ┃\n
    ┃                                                                                                              ┃\n
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n
        """
        try:
            async with ClientSession() as session:
                async with session.get(f"{self.api}/internal/player?key={self.key}&player={player}&overlay=true", headers=__header__) as response:
                    json = await response.json()
                    if not json["success"]:
                        raise InvalidAPIKeyError(self.key)
                    else:
                        if isinstance(json['data'], bool):
                            f = open(f"{resource_path('PolsuOverlay/PolsuAPI')}/schemas/nicked.json", mode="r", encoding="utf-8")
                            p = Player(load(f))
                            p.username = player
                            p.rank = f"§4[NICKED] §c{player}"
                            return p
                        else:
                            return Player(json.get('data'))
        except ContentTypeError:
            raise APIError
