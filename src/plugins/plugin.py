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
# This is the base plugin class, all plugins must have this format.
# Due to the way the plugin system works, you cannot inherit from this class
# since your plugin is outside of the Posu Overlay package.
#
# All methods are optional & parameters are optional.
# You mustn't change the name of your class, it must be "Plugin", instead you
# can change the name variable to whatever you want.
# The name variable is used to identify your plugin and is mandatory.
# All other variables are optional.
#
# A plugin can override some overlay internal methods, this is done by setting
# the OVERRIDE_<THE METHOD> variable to True.
# For example, if you want to override the on_player_load method, you would
# set OVERRIDE_on_player_load to True.
# This is useful if you want to do something instead of the overlay doing it.
#
# [!] WARNING: Only one plugin can override a method, if two plugins override
# the same method, the overlay will only load the first one!
#
# [>] NOTE: You don't need to override methods if you only want to do something 
# after the overlay has done it, you can just implement the method.
#
# If you have any questions, feel free to ask in the discord server!
# https://discord.polsu.xyz

class Plugin:
    """
    The base plugin class
    """
    name = "Plugin Example"

    disabled = False

    OVERRIDE_on_player_load = False
    OVERRIDE_on_search = False

    # Custom override, this doesn't override any overlay method but a small part
    # of the overlay code checks. If False it will use Polsu's global blacklist. 
    # If True, the plugin will handle the blacklist.
    OVERRIDE_global_blacklist = False

    logger: Logger
    blacklist: Type[TypeVar('PluginBlacklist')]
    notification: Type[TypeVar('PluginNotification')]
    table: Type[TypeVar('PluginTable')]
    logs: Type[TypeVar('PluginLogs')]
    api: Type[TypeVar('PluginAPI')]
    settings: Type[TypeVar('PluginSettings')]
    window: Type[TypeVar('PluginWindow')]
    player: Type[TypeVar('PluginPlayer')]

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
    

    def on_join(self, player: str) -> None:
        """
        Called when a player joins the game
        """
        raise NotImplementedError("on_join() is not implemented!")
    

    def on_leave(self, player: str) -> None:
        """
        Called when a player leaves the game
        """
        raise NotImplementedError("on_leave() is not implemented!")
    

    def on_final_kill(self, player: str) -> None:
        """
        Called when a player gets a final kill
        """
        raise NotImplementedError("on_final_kill() is not implemented!")
    

    def on_final_death(self, player: str) -> None:
        """
        Called when a player gets final killed
        """
        raise NotImplementedError("on_final_death() is not implemented!")
    

    def on_who(self) -> None:
        """
        Called when a player uses /who
        """
        raise NotImplementedError("on_who() is not implemented!")
    

    def on_list(self) -> None:
        """
        Called when a player uses /list
        """
        raise NotImplementedError("on_list() is not implemented!")
    

    def on_game_start(self) -> None:
        """
        Called when a game starts
        """
        raise NotImplementedError("on_game_start() is not implemented!")
