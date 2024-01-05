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
from src import DEV_MODE
from ..plugins.plugin import Plugin
from ..plugins.blacklist import PluginBlacklist
from ..plugins.notification import PluginNotification
from ..plugins.table import PluginTable
from ..plugins.logs import PluginLogs
from ..plugins.api import PluginAPI


import os
import importlib.util

from logging import Logger
from typing import Type, TypeVar


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
    ) -> None:
        """
        Initialise the class
        
        :param logger: The logger
        :param blacklist: The blacklist
        :param notification: The notification
        :param table: The table
        :param logs: The logs
        :param api: The API
        """
        self.logger = logger
        self.blacklist = blacklist
        self.notification = notification
        self.table = table
        self.logs = logs
        self.api = api

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
                    }

                    types = {
                        "logger": Logger,
                        "blacklist": Type[TypeVar('PluginBlacklist')],
                        "notification": Type[TypeVar('PluginNotification')],
                        "table": Type[TypeVar('PluginTable')],
                        "logs": Type[TypeVar('PluginLogs')],
                        "api": Type[TypeVar('PluginAPI')],
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


    def broadcast(self, method: str, *args, **kwargs) -> None:
        """
        Broadcast a method to all plugins
        
        :param method: The method to broadcast
        :param *args: The arguments to pass to the method
        :param **kwargs: The keyword arguments to pass to the method
        """
        if DEV_MODE:
            self.logger.debug(f"Broadcasting method, {method}, to all plugins")

        for plugin in self.__plugins:
            self.send(plugin.__name__, method, *args, **kwargs)

    
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
                if hasattr(p, method):
                    if DEV_MODE:
                        self.logger.debug(f"Sending method, {method}, to plugin: {plugin}")
                    
                    try:
                        getattr(p, method)(*args, **kwargs)
                    except NotImplementedError:
                        pass
                break
        else:
            self.logger.warning(f"Plugin: {plugin}, does not exist!")


    def getPlugins(self) -> list[Plugin]:
        """
        Get all plugins
        
        :return: A list of all plugins
        """
        return self.__plugins
    

    def askPlugins(self, constant: str) -> bool:
        """
        Ask all plugins for a variable
        
        :param constant: The constant to ask for
        :return: The response
        """
        for plugin in self.__plugins:
            if hasattr(plugin, constant):
                if getattr(plugin, f"CONST_{constant}", False):
                    self.logger.debug(f"Plugin: {plugin.__name__}, responded to constant: {constant}")
                    return True
        else:
            return False
