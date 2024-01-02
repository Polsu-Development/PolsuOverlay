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
from .blacklist import Blacklist
from ..utils.constants import CONFIG

import json 
import os

from typing import Union
from getpass import getuser


class Settings:
    """
    A class representing the overlay settings
    """
    def __init__(self, win) -> None:
        """
        Initialise the class
        
        :param win: The Overlay window
        """
        self.win = win


    def loadConfig(self) -> dict:
        """
        Load or create the config

        :return: The config
        """
        self.win.dirConfig = os.path.join(f"C:\\Users\\{getuser()}", 'Polsu', 'settings')
        self.win.themesConfig = os.path.join(f"C:\\Users\\{getuser()}", 'Polsu', 'themes')
        self.win.blacklistConfig = os.path.join(f"C:\\Users\\{getuser()}", 'Polsu', 'blacklist')

        if not os.path.exists(self.win.dirConfig):
            os.makedirs(self.win.dirConfig)
            self.win.newUser = True
        else:
            self.win.newUser = False

        # Create the themes and blacklist folders
        if not os.path.exists(self.win.themesConfig):
            os.makedirs(self.win.themesConfig)

        if not os.path.exists(self.win.blacklistConfig):
            os.makedirs(self.win.blacklistConfig)

        # Create the blacklist
        self.win.blacklist = Blacklist(self.win)

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
        self.win.confighideOverlay = config.get("hideOverlay", CONFIG.get('hideOverlay'))
        self.win.configXY = config.get("xy", CONFIG.get('xy'))
        self.win.configWH = config.get("wh", CONFIG.get('wh'))
        self.win.configStatus = config.get("status", CONFIG.get('status'))
        self.win.configSorting = config.get("sorting", CONFIG.get('sorting'))
        self.win.configRqColours = config.get("rqLevel", CONFIG.get('rqLevel'))
        self.win.configGlobalBlacklist = config.get("globalBlacklist", CONFIG.get('globalBlacklist'))
        
        return config


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
