from ..plugins.plugin import Plugin
from ..plugins.blacklist import PluginBlacklist
from ..plugins.notification import PluginNotification
from ..plugins.table import PluginTable


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
    ) -> None:
        """
        Initialise the class
        
        :param logger: The logger
        :param blacklist: The blacklist
        """
        self.logger = logger
        self.blacklist = blacklist
        self.notification = notification
        self.table = table

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
                    }

                    types = {
                        "logger": Logger,
                        "blacklist": Type[TypeVar('PluginBlacklist')],
                        "notification": Type[TypeVar('PluginNotification')],
                        "table": Type[TypeVar('PluginTable')],
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
                    self.logger.debug(f"Sending method, {method}, to plugin: {plugin}")
                    try:
                        getattr(p, method)(*args, **kwargs)
                    except NotImplementedError:
                        print(f"NotImplementedError {method} {args}")
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
