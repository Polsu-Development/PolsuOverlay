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
from ...components.blacklist import LocalBlacklisted
from ...utils.constants import TAGS


from time import time


class RequeueLevel:
    """
    A class representing the requeue level of a Hypixel Bedwars Player
    """
    def __init__(self, data) -> None:
        self._data = data

        try:
            self._index = int(data.get('index'))
        except:
            self._index = -1

        self._level = data.get('level')
        self._text = data.get('text')
        self._colour = data.get('colour')
        self._raw = data.get('raw')


    @property
    def data(self) -> dict:
        """
        The data of the user.
        """
        return self._data

    @property
    def index(self) -> int:
        """
        The Requeue Level index
        """
        return self._index
    
    @property
    def level(self) -> str:
        """
        The Requeue Level
        """
        return self._level
    
    @property
    def text(self) -> str:
        """
        The Requeue Level text
        """
        return self._text
    
    @property
    def colour(self) -> str:
        """
        The Requeue Level colour
        """
        return self._colour
    
    @colour.setter
    def colour(self, value: str) -> None:
        """
        Set the Requeue Level colour
        """
        self._colour = value
    
    @property
    def raw(self) -> str:
        """
        The Requeue Level raw
        """
        return self._raw
    

    def __repr__(self) -> str:
        return f"<RequeueLevel index={self.index} level={self.level} text={self.text} colour={self.colour} raw={self.raw}>"


class Mode:
    """
    A class representing a Bedwars mode
    """
    def __init__(self, data: dict, mode: str) -> None:
        self._data = data
        self._mode = mode

        self._games_played = data.get('games_played')
        self._winstreak = data.get('winstreak')
        self._kills = data.get('kills')
        self._deaths = data.get('deaths')
        self._kdr = data.get('kdr')
        self._fkills = data.get('fkills')
        self._fdeaths = data.get('fdeaths')
        self._fkdr = data.get('fkdr')
        self._wins = data.get('wins')
        self._losses = data.get('losses')
        self._wlr = data.get('wlr')
        self._broken = data.get('broken')
        self._lost = data.get('lost')
        self._bblr = data.get('bblr')
        self._requeue = RequeueLevel(data.get('rqlevel'))


    @property
    def data(self) -> dict:
        """
        The data of the user.
        """
        return self._data

    @property
    def mode(self) -> str:
        """
        The Bedwars mode
        """
        return self._mode
    
    @property
    def games_played(self) -> int:
        """
        The Bedwars games played
        """
        return self._games_played
    
    @property
    def winstreak(self) -> int:
        """
        The Bedwars winstreak
        """
        return self._winstreak
    
    @property
    def kills(self) -> int:
        """
        The Bedwars kills
        """
        return self._kills
    
    @property
    def deaths(self) -> int:
        """
        The Bedwars deaths
        """
        return self._deaths
    
    @property
    def kdr(self) -> float:
        """
        The Bedwars KDR
        """
        return self._kdr
    
    @property
    def fkills(self) -> int:
        """
        The Bedwars final kills
        """
        return self._fkills
    
    @property
    def fdeaths(self) -> int:
        """
        The Bedwars final deaths
        """
        return self._fdeaths
    
    @property
    def fkdr(self) -> float:
        """
        The Bedwars final KDR
        """
        return self._fkdr
    
    @property
    def wins(self) -> int:
        """
        The Bedwars wins
        """
        return self._wins
    
    @property
    def losses(self) -> int:
        """
        The Bedwars losses
        """
        return self._losses
    
    @property
    def wlr(self) -> float:
        """
        The Bedwars WLR
        """
        return self._wlr
    
    @property
    def broken(self) -> int:
        """
        The Bedwars beds broken
        """
        return self._broken
    
    @property
    def lost(self) -> int:
        """
        The Bedwars beds lost
        """
        return self._lost
    
    @property
    def bblr(self) -> float:
        """
        The Bedwars BBLR
        """
        return self._bblr
    
    @property
    def requeue(self) -> RequeueLevel:
        """
        The Bedwars Requeue Level
        """
        return self._requeue
    

    def __repr__(self) -> str:
        return f"<Bedwars formatted={self.formatted} stars={self.stars} games_played={self.games_played} winstreak={self.winstreak} kills={self.kills} deaths={self.deaths} kdr={self.kdr} fkills={self.fkills} fdeaths={self.fdeaths} fkdr={self.fkdr} wins={self.wins} losses={self.losses} wlr={self.wlr} beds={self.broken} broken={self.broken} bblr={self.bblr} requeue={self.requeue}>"


class Bedwars:
    """
    A class representing a Hypixel Bedwars Player
    """
    def __init__(self, data: dict) -> None:
        self._data = data

        self._formatted = data.get('formatted')
        self._stars = data.get('stars')
        self._games_played = data.get('games_played')
        self._winstreak = data.get('winstreak')
        self._kills = data.get('kills')
        self._deaths = data.get('deaths')
        self._kdr = data.get('kdr')
        self._fkills = data.get('fkills')
        self._fdeaths = data.get('fdeaths')
        self._fkdr = data.get('fkdr')
        self._wins = data.get('wins')
        self._losses = data.get('losses')
        self._wlr = data.get('wlr')
        self._broken = data.get('broken')
        self._lost = data.get('lost')
        self._bblr = data.get('bblr')
        self._requeue = RequeueLevel(data.get('rqlevel'))

        self.core = Mode(data.get('core'), 'core')
        self.solos = Mode(data.get('solos'), 'solos')
        self.doubles = Mode(data.get('doubles'), 'doubles')
        self.threes = Mode(data.get('threes'), 'threes')
        self.fours = Mode(data.get('fours'), 'fours')
        self.four_v_four = Mode(data.get('four_v_four'), '4v4')


    @property
    def data(self) -> dict:
        """
        The data of the user.
        """
        return self._data

    @property
    def formatted(self) -> str:
        """
        The Bedwars stars formatted
        """
        return self._formatted
    
    @property
    def stars(self) -> int:
        """
        The Bedwars stars
        """
        return self._stars
    
    @property
    def games_played(self) -> int:
        """
        The Bedwars games played
        """
        return self._games_played
    
    @property
    def winstreak(self) -> int:
        """
        The Bedwars winstreak
        """
        return self._winstreak
    
    @property
    def kills(self) -> int:
        """
        The Bedwars kills
        """
        return self._kills
    
    @property
    def deaths(self) -> int:
        """
        The Bedwars deaths
        """
        return self._deaths
    
    @property
    def kdr(self) -> float:
        """
        The Bedwars KDR
        """
        return self._kdr
    
    @property
    def fkills(self) -> int:
        """
        The Bedwars final kills
        """
        return self._fkills
    
    @property
    def fdeaths(self) -> int:
        """
        The Bedwars final deaths
        """
        return self._fdeaths
    
    @property
    def fkdr(self) -> float:
        """
        The Bedwars final KDR
        """
        return self._fkdr
    
    @property
    def wins(self) -> int:
        """
        The Bedwars wins
        """
        return self._wins
    
    @property
    def losses(self) -> int:
        """
        The Bedwars losses
        """
        return self._losses
    
    @property
    def wlr(self) -> float:
        """
        The Bedwars WLR
        """
        return self._wlr
    
    @property
    def broken(self) -> int:
        """
        The Bedwars beds broken
        """
        return self._broken
    
    @property
    def lost(self) -> int:
        """
        The Bedwars beds lost
        """
        return self._lost
    
    @property
    def bblr(self) -> float:
        """
        The Bedwars BBLR
        """
        return self._bblr
    
    @property
    def requeue(self) -> RequeueLevel:
        """
        The Bedwars Requeue Level
        """
        return self._requeue
    

    def __repr__(self) -> str:
        return f"<Bedwars formatted={self.formatted} stars={self.stars} games_played={self.games_played} winstreak={self.winstreak} kills={self.kills} deaths={self.deaths} kdr={self.kdr} fkills={self.fkills} fdeaths={self.fdeaths} fkdr={self.fkdr} wins={self.wins} losses={self.losses} wlr={self.wlr} beds={self.broken} broken={self.broken} bblr={self.bblr} requeue={self.requeue}>"


class Blacklisted:
    """
    A class representing a Hypixel Player
    """
    def __init__(self, data: dict) -> None:
        self._data = data

        self._status = data.get('status')
        self._reason = data.get('reason')


    @property
    def data(self) -> dict:
        """
        The data of the user.
        """
        return self._data
    
    @property
    def status(self) -> bool:
        """
        Whether the Player is blacklisted or not
        """
        return self._status
    
    @property
    def reason(self) -> str:
        """
        The Player blacklist reason
        """
        return self._reason
    

class Ping:
    """
    A class representing a Hypixel Player
    """
    def __init__(self, data: dict) -> None:
        self._data = data

        self._ping = data.get('ping', 0)
        self._timestamp = data.get('timestamp', -1)


    @property
    def data(self) -> dict:
        """
        The data of the user.
        """
        return self._data

    @property
    def ping(self) -> int:
        """
        The Player ping
        """
        return self._ping
    
    @property
    def timestamp(self) -> int:
        """
        The Player ping timestamp
        """
        return self._timestamp


class Player:
    """
    A class representing a Hypixel Player
    """
    def __init__(self, data: dict) -> None:
        self._data = data

        self._username = data.get('player').get('username')
        self._uuid = data.get('player').get('uuid')
        self._rank = data.get('player').get('rank')
        self._channel = data.get('player').get('channel')
        self._level = data.get('player').get('level')

        try:
            self._tag = TAGS[self.channel]
        except:
            self._tag = "§7-"

        self._cached = time()
        self._nicked = False

        self._bedwars = Bedwars(data.get('stats').get('Bedwars'))
        self._blacklisted = Blacklisted(data.get('blacklisted'))
        self._ping = Ping(data.get('ping'))
        self._local = None

        self._manual = False
        self._websocket = False


    @property
    def data(self) -> dict:
        """
        The data of the user.
        """
        return self._data

    @property
    def username(self) -> str:
        """
        The Player username
        """
        return self._username
    
    @username.setter
    def username(self, value: str) -> None:
        """
        Set the Player username
        """
        self._username = value

    @property
    def cleaned(self) -> str:
        """
        The Player username
        """
        return self.username.lower()

    @property
    def uuid(self) -> str:
        """
        The Player UUID
        """
        return self._uuid
    
    @property
    def rank(self) -> str:
        """
        The Player rank
        """
        return self._rank
    
    @rank.setter
    def rank(self, value: str) -> None:
        """
        Set the Player rank
        """
        self._rank = value
    
    @property
    def channel(self) -> str:
        """
        The Player channel
        """
        return self._channel
    
    @property
    def level(self) -> int:
        """
        The Player level
        """
        return self._level
    
    @property
    def tag(self) -> str:
        """
        The Player tag
        """
        return self._tag
    
    @property
    def cached(self) -> float:
        """
        The Player cache
        """
        return self._cached
    
    @property
    def nicked(self) -> bool:
        """
        Whether the Player is nicked or not
        """
        return self._nicked
    
    @nicked.setter
    def nicked(self, value: bool) -> None:
        """
        Set whether the Player is nicked or not
        """
        self._nicked = value

    @property
    def bedwars(self) -> Bedwars:
        """
        The Player Bedwars stats
        """
        return self._bedwars
    
    @property
    def blacklisted(self) -> Blacklisted:
        """
        The Player blacklist status
        """
        return self._blacklisted
    
    @property
    def ping(self) -> Ping:
        """
        The Player ping
        """
        return self._ping

    @property
    def local(self) -> LocalBlacklisted:
        """
        The Player blacklist status
        """
        return self._local
    

    @local.setter
    def local(self, value: LocalBlacklisted) -> None:
        """
        Set the Player local blacklist status
        """
        self._local = value


    @property
    def manual(self) -> bool:
        """
        Whether the Player is manually requested or not
        """
        return self._manual


    @manual.setter
    def manual(self, value: bool) -> None:
        """
        Set whether the Player is manually requested or not
        """
        self._manual = value


    @property
    def websocket(self) -> bool:
        """
        Whether the Player was requested through the WebSocket or not
        """
        return self._websocket
    

    @websocket.setter
    def websocket(self, value: bool) -> None:
        """
        Set whether the Player was requested through the WebSocket or not
        """
        self._websocket = value

    
    def __repr__(self) -> str:
        return f"<Player username={self.username} uuid={self.uuid} rank={self.rank} channel={self.channel} level={self.level} tag={self.tag} cached={self.cached} bedwars={self.bedwars}>"
    

    def __str__(self) -> str:
        return self.username
