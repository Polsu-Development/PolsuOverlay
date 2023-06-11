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
class Player:
    """
    A class representing a Hypixel Player
    """
    def __init__(self, data: dict) -> None:
        self.data = data

        self.username = data.get('player').get('username')
        self.uuid = data.get('player').get('uuid')
        self.rank = data.get('player').get('rank')
        self.channel = data.get('player').get('channel')
        self.level = data.get('player').get('level')
        self.tag = None

        self.bedwars = Bedwars(data.get('stats').get('Bedwars'))


    def getTag(self) -> str:
        """
        Returns a Player tag

        :return: A string reprensting the Player tag
        """
        d = {
            "ALL": "§7-",
            "PARTY": "§9[PARTY]",
        }

        try:
            return d[self.channel]
        except:
            return "§7-"


class Bedwars:
    """
    A class representing a Hypixel Bedwars Player
    """
    def __init__(self, data: dict) -> None:
        self.data = data

        self.formatted = data.get('formatted')
        self.stars = data.get('stars')
        self.games_played = data.get('games_played')
        self.winstreak = data.get('winstreak')
        self.kills = data.get('kills')
        self.deaths = data.get('deaths')
        self.kdr = data.get('kdr')
        self.fkills = data.get('fkills')
        self.fdeaths = data.get('fdeaths')
        self.fkdr = data.get('fkdr')
        self.wins = data.get('wins')
        self.losses = data.get('losses')
        self.wlr = data.get('wlr')
        self.beds = data.get('beds')
        self.broken = data.get('broken')
        self.bblr = data.get('bblr')
        self.quickbuy = data.get('quickbuy')
        self.requeue = RequeueLevel(data.get('rqlevel'))


class RequeueLevel:
    """
    A class representing the requeue level of a Hypixel Bedwars Player
    """
    def __init__(self, data) -> None:
        self.data = data

        try:
            self.index = int(data.get('index'))
        except:
            self.index = -1

        self.level = data.get('level')
        self.text = data.get('text')
        self.colour = data.get('colour')
        self.raw = data.get('raw')
