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
import re

from getpass import getuser

# Default configuration
CONFIG = {
    "APIKey": "",
    "client": "Vanilla",
    "logPath": f"/home/{getuser()}/.minecraft/logs/latest.log",
    "theme": "Default Dark",
    "opacity": 0.7,
    "RPC": True,
    "who": True,
    "status": True,
    "hideOverlay": True,
    "xy": [0, 0],
    "wh": [820, 400],
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

# Default Players Tags
TAGS = {
    "ALL": "§7-",
    "PARTY": "§9[PARTY]",
}

PLAYER_MESSAGE_PATTERN = re.compile(r'\[([A-Z0-9\+\-\*\s]+)\] \w+: .+') # [RANK] USERNAME: MESSAGE

CLIENT_NAMES = [
    "Minecraft",
    "Lunar Client",
    "Lunar",
    "Badlion Client",
    "Badlion",
]

SUFFIX_SVG_MAP = {
    "🐷": "techno.svg",
    "👑": "owner.svg",
    "🔨": "staff.svg",
    "💻": "dev.svg",
    "🔗": "partner.svg",
    "✨": "premium.svg",
}
