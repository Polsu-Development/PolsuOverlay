from ..utils.plugin import Plugin


import os
import importlib.util

from logging import Logger


class PluginCore:
    """
    A class representing the plugin core
    """
    def __init__(
        self, 
        logger: Logger
    ) -> None:
        """
        Initialise the class
        
        :param logger: The logger
        :param user: The user
        """
        self.logger = logger

        self.plugins = []


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
                        self.logger.warning(f"Invalid constructor signature in Plugin class of module {module_name}")
                        continue

                    arguments = {
                        "logger": self.logger
                    }

                    plugin_arguments = {}

                    # Get the arguments for the Plugin class
                    for arg_name, arg_type in constructor.__annotations__.items():
                        if arg_name in arguments:
                            plugin_arguments[arg_name] = arguments[arg_name]

                    # Create the plugin
                    plugin: Plugin = plugin_class(**plugin_arguments)
                    plugin.__name__ = plugin.name
                    self.plugins.append(plugin)

                    # Call the on_load method
                    self.logger.info(f"Loaded plugin {plugin.__name__}")
                    self.send(plugin.__name__, "on_load")
                else:
                    self.logger.warning(f"No Plugin class found in module {module_name}")


    def unload_plugins(self) -> None:
        """
        Unload all plugins
        """
        for plugin in self.plugins:
            self.logger.info(f"Unloaded plugin {plugin.__name__}")

            self.send(plugin.__name__, "on_unload")

        self.plugins = []


    def broadcast(self, method: str, *args, **kwargs) -> None:
        """
        Broadcast a method to all plugins
        
        :param method: The method to broadcast
        :param *args: The arguments to pass to the method
        :param **kwargs: The keyword arguments to pass to the method
        """
        for plugin in self.plugins:
            if hasattr(plugin, method):
                getattr(plugin, method)(*args, **kwargs)
                self.logger.debug(f"Broadcasted method {method} to plugin {plugin.__name__}")

    
    def send(self, plugin: str, method: str, *args, **kwargs) -> None:
        """
        Send a method to a plugin
        
        :param plugin: The plugin to send the method to
        :param method: The method to send
        :param *args: The arguments to pass to the method
        :param **kwargs: The keyword arguments to pass to the method
        """
        for p in self.plugins:
            if p.__name__ == plugin:
                if hasattr(p, method):
                    getattr(p, method)(*args, **kwargs)
                    self.logger.debug(f"Sent method {method} to plugin {plugin}")
                else:
                    self.logger.warning(f"Plugin {plugin} does not have method {method}!")
                break
        else:
            self.logger.warning(f"Plugin {plugin} does not exist!")
