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

    logger: Logger
    blacklist: Type[TypeVar('PluginBlacklist')]
    notification: Type[TypeVar('PluginNotification')]
    table: Type[TypeVar('PluginTable')]

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
