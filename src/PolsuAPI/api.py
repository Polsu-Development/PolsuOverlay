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
from src import __header__, DEV_MODE
from ..utils.path import resource_path

from .objects.key import APIKey
from .objects.player import Player
from .objects.user import User
from .exception import APIError, InvalidAPIKeyError, NotLinkedError


import traceback

from aiohttp import ClientSession, ContentTypeError, WSMsgType
from json import load


class Polsu:
    """
    A class representing the Polsu API
    """
    def __init__(self, key: str, logger) -> None:
        self.key = key
        self.logger = logger

        # The current API base url
        self.api = "https://api.polsu.xyz"

        self.polsuHeaders = __header__
        self.polsuHeaders["API-Key"] = self.key
    

    async def get_key_stats(self) -> APIKey:
        """
        Get the Polsu API Key stats

        :return: An instance of APIKey
        """
        try:
            if DEV_MODE:
                self.logger.info(f"GET /api/key?key={self.key}")

            async with ClientSession() as session:
                async with session.get(f"{self.api}/api/key", headers=self.polsuHeaders) as response:
                    json = await response.json()
                    if response.status == 403:
                        raise InvalidAPIKeyError(self.key)
                    elif response.status in [404, 422, 500]:
                        self.logger.error(f"An error occurred while getting the API Key stats: {response.status}")
                        return response.status
                    elif not json["success"]:
                        raise APIError
                    else:
                        return APIKey(json)
        except ContentTypeError:
            raise APIError
        except Exception as e:
            self.logger.error(f"An error occurred while getting the key stats!\n\nTraceback: {traceback.format_exc()} | {e}")
            return None
        

    async def login(self) -> User:
        """
        Get the current user UUID & Minecraft Username

        :return: An instance of User


    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n
    ┃                                                                                                              ┃\n
    ┃                                               >> WARNING <<                                                  ┃\n
    ┃                                                                                                              ┃\n
    ┃  • The following endpoint, '/internal/overlay/login' is a private endpoint.                                  ┃\n
    ┃                                                                                                              ┃\n
    ┃  > IT IS STRICTLY FORBIDDEN TO USE IT OUTSIDE POLSU'S OFFICIAL OVERLAY.                                      ┃\n
    ┃  > ANY USAGE OF THIS ENDPOINT FOR OTHER PROJECTS OR FORKS OF POLSU'S OVERLAY ISN'T ALLOWED!                  ┃\n
    ┃                                                                                                              ┃\n
    ┃  • If we notice any suspicious activity on this endpoint, following our Terms of Services, your api key and  ┃\n
    ┃    therefore your Discord account, will get blacklisted from our Services!                                   ┃\n
    ┃  > This means you won't be able to use any of our Services anymore, including Polsu and Polsu's Overlay.     ┃\n
    ┃                                                                                                              ┃\n
    ┃  • Note: This warning applies to all endpoints starting with: '/internal'                                    ┃\n
    ┃  > You are only allowed to use the public endpoints, listed in the documentation at: https://api.polsu.xyz   ┃\n
    ┃                                                                                                              ┃\n
    ┃                                                                                                              ┃\n
    ┃  • If you have any questions, don't hesitate to contact us on discord at: https://discord.polsu.xyz.         ┃\n
    ┃                                                                                                              ┃\n
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n
        """
        try:
            if DEV_MODE:
                self.logger.info(f"GET /internal/overlay/login?overlay=true")

            async with ClientSession() as session:
                async with session.get(f"{self.api}/internal/overlay/login?overlay=true", headers=self.polsuHeaders) as response:
                    json = await response.json()
                    if response.status == 403:
                        self.logger.error(f"An error occurred while logging in: {response.status}")
                        raise InvalidAPIKeyError(self.key)
                    elif response.status in [404, 422, 500]:
                        self.logger.error(f"An error occurred while logging in: {response.status}")
                        return response.status
                    elif not json["success"]:
                        raise APIError
                    else:
                        if json.get('data', {}) == {}:
                            raise NotLinkedError()
                        else:
                            return User(json.get('data'))
        except ContentTypeError:
            raise APIError
        except Exception as e:
            self.logger.error(f"An error occurred while logging in!\n\nTraceback: {traceback.format_exc()} | {e}")
            return None
        
    
    async def WebSocketConnection(self, setWebSocket, callback, closed) -> None:
        """
        Create a WebSocket connection

        :param setWebSocket: A function to set the WebSocket
        :param callback: A function to call when a player is received
        :param closed: A function to call when the WebSocket is closed
        """
        self.logger.info(f"[WS] Creating a WebSocket connection...")

        # Wait for messages
        expired = False

        try:
            # Create a WebSocket connection
            async with ClientSession() as session:
                async with session.ws_connect(
                    url=f"{self.api}/internal/overlay/websocket", 
                    headers=self.polsuHeaders, 
                    timeout=1800, 
                    receive_timeout=1800,
                    heartbeat=1800,
                    autoping=True,
                    autoclose=False
                ) as ws:
                    if not ws.closed:
                        self.logger.info(f"[WS] Starting websocket connection...")
                        self.logger.debug(f"[WS] Sending handshake...")

                        # Send a handshake
                        await ws.send_json(
                            {
                                "protocol": "PolsuWebSocketProtocol - 1.0",
                                "handshake": self.key
                            }
                        )

                        self.logger.debug(f"[WS] Handshake sent!")

                    if not ws.closed:
                        # Wait for the handshake response
                        async for msg in ws:
                            try:
                                data = msg.json()
                                if data.get('success', False) and data.get('data', {}) == "Connection established.":
                                    self.logger.info(f"[WS] New WebSocket connection established!")
                                    break
                                else:
                                    self.logger.debug(f"[WS] Couldn't create a WebSocket connection! {msg}")
                                    break
                            except:
                                self.logger.debug(f"[WS] Couldn't create a WebSocket connection! {msg}")
                                break

                    if not ws.closed:
                        # Set the WebSocket so the overlay can send messages
                        await setWebSocket(ws)

                        self.logger.info(f"[WS] WebSocket connection established!")

                        async for msg in ws:
                            if msg.type in (WSMsgType.CLOSED, WSMsgType.ERROR):
                                return
                            else:
                                try:
                                    data = msg.json()

                                    if DEV_MODE:
                                        self.logger.debug(f"[WS] Received data: {data}")

                                    if data.get("data", {}) != {}:
                                        if data.get("success", False):
                                            player = Player(data.get("data"))
                                            player.manual = data.get("data", {}).get("player", {}).get("manual", False)
                                            player.websocket = True
                                            await callback(player)
                                        else:
                                            if isinstance(data.get("data", {}), str):
                                                if data.get("data", {}) == "Expired websocket!":
                                                    self.logger.warning(f"[WS] WebSocket connection expired!")
                                                    expired = True

                                                    raise Exception("Expired websocket!")
                                                elif data.get("data", {}) == "Packet limit reached!":
                                                    self.logger.error(f"[WS] Packet limit reached!")
                                                    expired = True

                                                    raise Exception("Packet limit reached!")
                                                elif data.get("data", {}) == "Malformed JSON" or data.get("data", {}) == "Missing query" or data.get("data", {}) == "Invalid query":
                                                    self.logger.error(f"[WS] An error occurred while sending some data: {data.get('data', {})}")
                                                elif data.get("data", {}) == "Too many players":
                                                    self.logger.error(f"[WS] Oops we reached the maximum amount of players!")
                                                else:
                                                    self.logger.error(f"[WS] An error occurred with the websocket connection: {data.get('data', {})}")
                                            else:
                                                if data.get("cause", None).startswith("Rate Limited"):
                                                    self.logger.error(f"[WS] Rate limited! {data.get('cause', None)}")

                                                    raise Exception("Rate limited!")
                                                else:
                                                    f = open(f"{resource_path('src/PolsuAPI')}/schemas/nicked.json", mode="r", encoding="utf-8")
                                                    player = Player(load(f))
                                                    player.username = data.get("data", {}).get("player", {}).get("username")
                                                    player.rank = f"§c{data.get('data', {}).get('player', {}).get('username')}"
                                                    player.manual = data.get("data", {}).get("player", {}).get("manual", False)
                                                    player.nicked = True
                                                    player.websocket = True
                                                    await callback(player)
                                except Exception as e:
                                    self.logger.error(f"An error occurred while receiving a WebSocket message!\n\nTraceback: {traceback.format_exc()} | {e}")
        except Exception as e:
            self.logger.error(f"An error occurred while creating a WebSocket connection!\n\nTraceback: {traceback.format_exc()} | {e}")
        
        closed(expired)

        self.logger.info(f"[WS] WebSocket connection closed!")


    async def get_stats(self, player: str) -> Player:
        """
        Get a Player Hypixel Stats

        :param player: A player (username or uuid)
        :return: An instance of Player


    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n
    ┃                                                                                                              ┃\n
    ┃                                               >> WARNING <<                                                  ┃\n
    ┃                                                                                                              ┃\n
    ┃  • The following endpoint, '/internal/overlay/player' is a private endpoint.                                 ┃\n
    ┃                                                                                                              ┃\n
    ┃  > IT IS STRICTLY FORBIDDEN TO USE IT OUTSIDE POLSU'S OFFICIAL OVERLAY.                                      ┃\n
    ┃  > ANY USAGE OF THIS ENDPOINT FOR OTHER PROJECTS OR FORKS OF POLSU'S OVERLAY ISN'T ALLOWED!                  ┃\n
    ┃                                                                                                              ┃\n
    ┃  • If we notice any suspicious activity on this endpoint, following our Terms of Services, your api key and  ┃\n
    ┃    therefore your Discord account, will get blacklisted from our Services!                                   ┃\n
    ┃  > This means you won't be able to use any of our Services anymore, including Polsu and Polsu's Overlay.     ┃\n
    ┃                                                                                                              ┃\n
    ┃  • Note: This warning applies to all endpoints starting with: '/internal'                                    ┃\n
    ┃  > You are only allowed to use the public endpoints, listed in the documentation at: https://api.polsu.xyz   ┃\n
    ┃                                                                                                              ┃\n
    ┃                                                                                                              ┃\n
    ┃  • If you have any questions, don't hesitate to contact us on discord at: https://discord.polsu.xyz.         ┃\n
    ┃                                                                                                              ┃\n
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n
        """
        try:
            if DEV_MODE:
                self.logger.info(f"GET /internal/overlay/player?player={player}&overlay=true")

            async with ClientSession() as session:
                async with session.get(f"{self.api}/internal/overlay/player?player={player}&overlay=true", headers=self.polsuHeaders) as response:
                    json = await response.json()

                    if DEV_MODE:
                        self.logger.debug(f"[{response.status}] {player} > {json}")

                    if response.status == 403:
                        self.logger.error(f"An error occurred while getting player stats: {response.status}")
                        raise InvalidAPIKeyError(self.key)
                    elif response.status in [404, 422, 500]:
                        self.logger.error(f"An error occurred while getting player stats: {response.status}")
                        return response.status
                    elif not json["success"]:
                        raise APIError
                    else:
                        if isinstance(json['data'], bool):
                            f = open(f"{resource_path('src/PolsuAPI')}/schemas/nicked.json", mode="r", encoding="utf-8")
                            p = Player(load(f))
                            p.username = player
                            p.rank = f"§c{player}"
                            p.nicked = True
                            return p
                        else:
                            return Player(json.get('data'))
        except ContentTypeError:
            raise APIError
        except Exception as e:
            self.logger.error(f"An error occurred while getting the stats of {player}!\n\nTraceback: {traceback.format_exc()} | {e}")
            return None


    async def post_stats(self, players: list) -> Player:
        """
        Get a Player Hypixel Stats

        :param players: A list of players (username or uuid)
        :return: An instance of Player


    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n
    ┃                                                                                                              ┃\n
    ┃                                               >> WARNING <<                                                  ┃\n
    ┃                                                                                                              ┃\n
    ┃  • The following endpoint, '/internal/overlay/player' is a private endpoint.                                 ┃\n
    ┃                                                                                                              ┃\n
    ┃  > IT IS STRICTLY FORBIDDEN TO USE IT OUTSIDE POLSU'S OFFICIAL OVERLAY.                                      ┃\n
    ┃  > ANY USAGE OF THIS ENDPOINT FOR OTHER PROJECTS OR FORKS OF POLSU'S OVERLAY ISN'T ALLOWED!                  ┃\n
    ┃                                                                                                              ┃\n
    ┃  • If we notice any suspicious activity on this endpoint, following our Terms of Services, your api key and  ┃\n
    ┃    therefore your Discord account, will get blacklisted from our Services!                                   ┃\n
    ┃  > This means you won't be able to use any of our Services anymore, including Polsu and Polsu's Overlay.     ┃\n
    ┃                                                                                                              ┃\n
    ┃  • Note: This warning applies to all endpoints starting with: '/internal'                                    ┃\n
    ┃  > You are only allowed to use the public endpoints, listed in the documentation at: https://api.polsu.xyz   ┃\n
    ┃                                                                                                              ┃\n
    ┃                                                                                                              ┃\n
    ┃  • If you have any questions, don't hesitate to contact us on discord at: https://discord.polsu.xyz.         ┃\n
    ┃                                                                                                              ┃\n
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n
        """
        json = {
            "players": players
        }

        try:
            if DEV_MODE:
                self.logger.info(f"POST /internal/overlay/player?overlay=true")

            async with ClientSession() as session:
                async with session.post(f"{self.api}/internal/overlay/player?overlay=true", headers=self.polsuHeaders, json=json) as response:
                    json = await response.json()
                    if response.status == 403:
                        self.logger.error(f"An error occurred while getting player stats: {response.status}")
                        raise InvalidAPIKeyError(self.key)
                    elif response.status in [404, 422, 500]:
                        self.logger.error(f"An error occurred while getting player stats: {response.status}")
                        return response.status
                    elif not json:
                        raise APIError
                    else:
                        data = []
                        for i, p in enumerate(json.get('data')):
                            if isinstance(p, bool):
                                f = open(f"{resource_path('src/PolsuAPI')}/schemas/nicked.json", mode="r", encoding="utf-8")
                                p = Player(load(f))
                                p.username = players[i]
                                p.rank = f"§c{players[i]}"
                                p.nicked = True
                                data.append(p)
                            else:
                                data.append(Player(p.get('data')))
                        return data
        except ContentTypeError:
            raise APIError
        except Exception as e:
            self.logger.error(f"An error occurred while getting the stats of {players}!\n\nTraceback: {traceback.format_exc()} | {e}")
            return None


    async def load_quickbuy(self, uuid: str) -> None:
        """
        Load the Player quickbuy

        :param uuid: The Player uuid
        """
        try:
            if DEV_MODE:
                self.logger.info(f"GET /polsu/bedwars/quickbuy?uuid={uuid}")

            async with ClientSession() as session:
                async with session.get(f"{self.api}/polsu/bedwars/quickbuy?uuid={uuid}", headers=self.polsuHeaders) as response:
                    json = await response.json()
                    if response.status == 403:
                        self.logger.error(f"An error occurred while getting player quickbuy: {response.status}")
                        raise InvalidAPIKeyError(self.key)
                    elif response.status in [404, 422, 500]:
                        self.logger.error(f"An error occurred while getting player quickbuy {response.status}")
                        return response.status
                    elif not json["success"]:
                        raise APIError
                    else:
                        if json.get('data', {}).get('image', None):
                            async with session.get(json.get('data', {}).get('image'), headers=self.polsuHeaders) as response:
                                return await response.read()
                        else:
                            raise APIError
        except ContentTypeError:
            raise APIError
        except Exception as e:
            self.logger.error(f"An error occurred while getting the quickbuy of {uuid}!\n\nTraceback: {traceback.format_exc()} | {e}")
            return None

    
    async def load_skin(self, player: Player) -> None:
        """
        Load the Player skin

        :param player: The Player
        """
        try:
            if DEV_MODE:
                self.logger.info(f"GET skins.mcstats.com/face/{player.uuid}")

            headers = {
                "User-Agent": __header__["User-Agent"]
            }

            async with ClientSession() as session:
                async with session.get(f"https://skins.mcstats.com/face/{player.uuid}", headers=headers) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        self.logger.error(f"An error occurred while getting the skin of {player.uuid} ({response.status})!")
                        raise APIError
        except ContentTypeError:
            return None
        except APIError:
            return None
        except Exception as e:
            self.logger.error(f"An error occurred while getting the skin of {player.uuid}!\n\nTraceback: {traceback.format_exc()} | {e}")
            return None
