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
from ..PolsuAPI import Player, User


from logging import Logger
from typing import Type, TypeVar


# Plugin class
#
# You musn't change the name of this class!
class Plugin:
    """
    The base plugin class
    """
    name = "Plugin"

    disabled = False

    CONST_on_player_load = False

    logger: Logger
    blacklist: Type[TypeVar('PluginBlacklist')]
    notification: Type[TypeVar('PluginNotification')]
    table: Type[TypeVar('PluginTable')]
    api: Type[TypeVar('PluginAPI')]

    def __init__(self) -> None:
        """
        Initialise the plugin
        """
        pass
    

    def on_load(self) -> None:
        """
        Called when the plugin is loaded
        """
        raise NotImplementedError("on_load() is not implemented!")
    

    def on_unload(self) -> None:
        """
        Called when the plugin is unloaded
        """
        raise NotImplementedError("on_unload() is not implemented!")
    

    def on_login(self, user: User) -> None:
        """
        Called when the user logs in
        """
        raise NotImplementedError("on_login() is not implemented!")
    

    def on_logout(self, user: User) -> None:
        """
        Called when the user logs out
        """
        raise NotImplementedError("on_logout() is not implemented!")
    

    def on_search(self, player: str) -> None:
        """
        Called before the user searches for a player
        """
        raise NotImplementedError("before_search() is not implemented!")


    def on_player_load(self, player: str) -> None:
        """
        Called when the player is loaded
        """
        raise NotImplementedError("on_player_load() is not implemented!")
    

    def on_player_insert(self, player: Player) -> None:
        """
        Called when the player is inserted
        """
        raise NotImplementedError("on_insert() is not implemented!")


    def on_player_message(self, message: str) -> None:
        """
        Called when the player sends a message
        """
        raise NotImplementedError("on_player_message() is not implemented!")
    

    def on_message(self, message: str) -> None:
        """
        Called when a message is sent
        """
        raise NotImplementedError("on_message() is not implemented!")
