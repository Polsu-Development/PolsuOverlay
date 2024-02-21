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
from src import DEV_MODE
from ..plugins.plugin import Plugin
from ..plugins.blacklist import PluginBlacklist
from ..plugins.notification import PluginNotification
from ..plugins.table import PluginTable
from ..plugins.logs import PluginLogs
from ..plugins.api import PluginAPI
from ..plugins.settings import PluginSettings
from ..plugins.window import PluginWindow
from ..plugins.player import PluginPlayer


import os
import importlib.util
import traceback

from logging import Logger
from typing import Type, TypeVar


# Please check src/plugins/plugin.py for more information about how plugins work!
class PluginCore:
    """
    A class representing the plugin core
    """
    def __init__(
        self, 
        logger: Logger,
        blacklist: PluginBlacklist,
        notification: PluginNotification,
        table: PluginTable,
        logs: PluginLogs,
        api: PluginAPI,
        settings: PluginSettings,
        window: PluginWindow,
        player: PluginPlayer,
    ) -> None:
        """
        Initialise the class
        
        :param logger: The logger
        :param blacklist: The blacklist
        :param notification: The notification
        :param table: The table
        :param logs: The logs
        :param api: The API
        :param settings: The settings
        :param window: The window
        :param player: The player
        """
        self.logger = logger
        self.blacklist = blacklist
        self.notification = notification
        self.table = table
        self.logs = logs
        self.api = api
        self.settings = settings
        self.window = window
        self.player = player

        self.__plugins = []


    def load_plugins(self, path: str) -> None:
        """
        Load plugins from a given path
        
        :param path: The path to load plugins from
        """
        if not os.path.exists(path):
            self.logger.warning(f"Path {path} does not exist!")
            return

        for file_name in os.listdir(path):
            if file_name.endswith(".py"):
                module_name = file_name[:-3]
                module_path = os.path.join(path, file_name)

                # Load the module
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Check if the module has a Plugin class
                if hasattr(module, "Plugin"):
                    plugin_class = module.Plugin

                    # Check if the Plugin class has a valid constructor
                    constructor = getattr(plugin_class, "__init__", None)
                    if constructor is None or not hasattr(constructor, "__annotations__"):
                        self.logger.warning(f"Invalid constructor signature in Plugin class of module: {module_name}")
                        continue

                    arguments = {
                        "logger": self.logger,
                        "blacklist": self.blacklist,
                        "notification": self.notification,
                        "table": self.table,
                        "logs": self.logs,
                        "api": self.api,
                        "settings": self.settings,
                        "window": self.window,
                        "player": self.player,
                    }

                    types = {
                        "logger": Logger,
                        "blacklist": Type[TypeVar('PluginBlacklist')],
                        "notification": Type[TypeVar('PluginNotification')],
                        "table": Type[TypeVar('PluginTable')],
                        "logs": Type[TypeVar('PluginLogs')],
                        "api": Type[TypeVar('PluginAPI')],
                        "settings": Type[TypeVar('PluginSettings')],
                        "window": Type[TypeVar('PluginWindow')],
                        "player": Type[TypeVar('PluginPlayer')],
                    }

                    plugin_arguments = {}

                    # Get the arguments for the Plugin class
                    for arg_name, arg_type in constructor.__annotations__.items():
                        if arg_name not in ["self", "return"]:
                            if arg_name in arguments:
                                expected_type = types.get(arg_name)
                                if expected_type is not None:
                                    # Check if the string representation of types are equal
                                    if str(arg_type) != str(expected_type):
                                        self.logger.error(f"Invalid type for argument, {arg_name}, in Plugin class of module: {module_name}. Expected {expected_type}, got {arg_type}")
                                        break
                                    else:
                                        plugin_arguments[arg_name] = arguments[arg_name]
                                else:
                                    self.logger.error(f"Unexpected argument, {arg_name}, in Plugin class of module: {module_name}")
                                    break
                    else:
                        # Create the plugin
                        try:
                            plugin: Plugin = plugin_class(**plugin_arguments)
                            plugin.__name__ = plugin.name
                        except TypeError:
                            self.logger.error(f"Invalid arguments for Plugin class of module: {module_name}")
                            continue

                        if hasattr(plugin, "disabled") and plugin.disabled:
                            self.logger.warning(f"Plugin: {plugin.__name__}, is disabled")
                            continue


                        # Check if overrides of plugins already exists
                        overrides = self.getAllOverrides()

                        for override in self.getPluginOverrides(plugin):
                            if override in overrides:
                                self.logger.warning(f"Plugin: {plugin.__name__}, has a override that already exists: {override}")
                                continue


                        self.__plugins.append(plugin)

                        # Call the on_load method
                        self.logger.info(f"Loaded plugin: {plugin.__name__}")
                        self.send(plugin.__name__, "on_load")
                else:
                    self.logger.warning(f"No Plugin class found in module: {module_name}")


    def unload_plugins(self) -> None:
        """
        Unload all plugins
        """
        for plugin in self.__plugins:
            self.logger.info(f"Unloaded plugin: {plugin.__name__}")

            self.send(plugin.__name__, "on_unload")

        self.__plugins = []


    def disable_plugin(self, plugin: Plugin) -> None:
        """
        Disable a plugin
        
        :param plugin: The plugin to disable
        """
        if plugin not in self.__plugins:
            self.logger.warning(f"Plugin: {plugin.__name__}, isn't loaded! Cannot disable it...")
            return
        else:
            self.__plugins.remove(plugin)

            self.logger.warning(f"Disabled plugin: {plugin.__name__}")


    def broadcast(self, method: str, *args, override: bool = False, **kwargs) -> None:
        """
        Broadcast a method to all plugins
        
        :param method: The method to broadcast
        :param *args: The arguments to pass to the method
        :param override: Whether to override the overlay function
        :param **kwargs: The keyword arguments to pass to the method
        """
        if DEV_MODE:
            self.logger.debug(f"Broadcasting method, {method}, to all plugins")

        try:
            for plugin in self.__plugins:
                kwargs["override"] = override
                self.send(plugin.__name__, method, *args, **kwargs)
        except:
            self.logger.error(f"An error occurred while broadcasting method, {method}, to all plugins!\n\nTraceback: {traceback.format_exc()}")


    def send(self, plugin: str, method: str, *args, **kwargs) -> None:
        """
        Send a method to a plugin
        
        :param plugin: The plugin to send the method to
        :param method: The method to send
        :param *args: The arguments to pass to the method
        :param **kwargs: The keyword arguments to pass to the method
        """
        for p in self.__plugins:
            if p.__name__ == plugin:
                if p.disabled:
                    self.disable_plugin(p)
                    continue

                if hasattr(p, method):
                    if DEV_MODE:
                        self.logger.debug(f"Sending method, {method}, to plugin: {plugin}")

                    # Check if the method has the arguments
                    new_kwargs = {}
                    for key, value in kwargs.items():
                        if key in getattr(p, method).__code__.co_varnames:
                            new_kwargs[key] = value

                    try:
                        getattr(p, method)(*args, **new_kwargs)
                    except NotImplementedError:
                        pass
                    except:
                        self.logger.error(f"An error occurred while sending method, {method}, to plugin: {plugin}\n\nTraceback: {traceback.format_exc()}")
                break
        else:
            self.logger.warning(f"Plugin: {plugin}, does not exist!")


    def getPlugins(self) -> list[Plugin]:
        """
        Get all plugins
        
        :return: A list of all plugins
        """
        return self.__plugins


    def askPlugins(self, override: str) -> bool:
        """
        Ask all plugins for a variable
        
        :param override: The override to ask for
        :return: The response
        """
        for plugin in self.__plugins:
            if self.askPlugin(plugin, override):
                return True
        else:
            return False


    def askPlugin(self, plugin: Plugin, override: str):
        """
        Ask a plugin for a variable
        
        :param plugin: The plugin to ask
        :param override: The override to ask for
        :return: The response
        """
        if plugin.disabled:
            self.disable_plugin(plugin) 
            return False

        if hasattr(plugin, f"OVERRIDE_{override}"):
            if getattr(plugin, f"OVERRIDE_{override}", False):
                if DEV_MODE:
                    self.logger.debug(f"Plugin: {plugin.__name__}, responded to override: {override}")
                return True
        else:
            return False


    def getPluginOverrides(self, plugin: Plugin) -> list:
        """
        Get all overrides of a plugin

        :param plugin: The plugin instance
        :return: A list of overrides
        """
        return list(filter(lambda override: self.askPlugin(plugin, override.replace("OVERRIDE_", "")), [attr for attr in dir(plugin) if not callable(getattr(plugin, attr)) and attr.startswith("OVERRIDE_")]))


    def getAllOverrides(self) -> list:
        """
        Get all overrides of all plugins
        
        :return: A list of overrides
        """
        overrides = []

        for plugin in self.__plugins:
            overrides.extend(self.getPluginOverrides(plugin))

        return overrides
