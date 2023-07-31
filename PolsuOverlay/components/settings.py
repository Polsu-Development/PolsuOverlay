from getpass import getuser

import json 
import os

from typing import Union


# Default configuration
CONFIG = {
    "APIKey": "",
    "client": "Vanilla",
    "logPath": f"C:\\Users\\{getuser()}\\AppData\\Roaming\\.minecraft\\logs\\latest.log",
    "theme": "Default Dark",
    "opacity": 0.5,
    "RPC": True,
    "who": True,
    "passThrough": True,
    "xy": [0, 0],
    "wh": [820, 400],
    "status": True,
    "sorting": [2, 0],
    "rqLevel": {
        "-1": "AAAAAA",
        "0": "AAAAAA",
        "1": "55FF55",
        "2": "55FF55",
        "3": "FFFF55",
        "4": "FFFF55",
        "5": "FFAA00",
        "6": "FFAA00",
        "7": "FF5555",
        "8": "FF5555",
        "9": "AA0000",
        "10": "AA0000",
        "11": "5555FF",
        "12": "FF55FF"
    }
}


class Settings:
    """
    A class representing the overlay settings
    """
    def __init__(self, win) -> None:
        self.win = win


    def loadConfig(self) -> None:
        """
        Load or create the config
        """
        self.win.dirConfig = os.path.join(f"C:\\Users\\{getuser()}", 'Polsu', 'settings')
        self.win.themesConfig = os.path.join(f"C:\\Users\\{getuser()}", 'Polsu', 'themes')

        if not os.path.exists(self.win.dirConfig):
            os.makedirs(self.win.dirConfig)
            os.makedirs(self.win.themesConfig)
            self.win.newUser = True
        else:
            self.win.newUser = False

        self.win.pathConfig = os.path.join(self.win.dirConfig, "data.json")

        try:
            with open(self.win.pathConfig, "r") as f:
                config = json.load(f)
        except:
            with open(self.win.pathConfig, "w") as f:
                json.dump(CONFIG, f, indent=6)
            config = CONFIG

        self.win.configAPIKey = config.get("APIKey", CONFIG.get('APIKey'))
        self.win.configClient = config.get("client", CONFIG.get('client'))
        self.win.configLogPath = config.get("logPath", CONFIG.get('logPath'))
        self.win.configTheme = config.get("theme", CONFIG.get('theme'))
        self.win.configOpacity = config.get("opacity", CONFIG.get('opacity'))
        self.win.configRPC = config.get("RPC", CONFIG.get('RPC'))
        self.win.configWho = config.get("who", CONFIG.get('who'))
        self.win.configPassThrough = config.get("passThrough", CONFIG.get('passThrough'))
        self.win.configXY = config.get("xy", CONFIG.get('xy'))
        self.win.configWH = config.get("wh", CONFIG.get('wh'))
        self.win.configStatus = config.get("status", CONFIG.get('status'))
        self.win.configSorting = config.get("sorting", CONFIG.get('sorting'))
        self.win.configRqColours = config.get("rqLevel", CONFIG.get('rqLevel'))


    def update(self, key: str, setting: Union[str, bool, list, dict]) -> None:
        """
        Update a setting

        :param key: Setting key (e.g. 'APIKey')
        :param setting: Setting value
        """
        with open(self.win.pathConfig, "r") as f:
            config = json.load(f)

        config[key] = setting

        with open(self.win.pathConfig, "w") as f:
            json.dump(config, f, indent=6)
