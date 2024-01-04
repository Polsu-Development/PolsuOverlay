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
import os


class PlayerBlacklist:
    """
    A class representing a Player Blacklist
    """
    def __init__(self, player: str, reason: str) -> None:
        """
        Initialise the class
        
        :param player: The player
        :param reason: The reason
        """
        self._player = player
        self._reason = reason


    @property
    def player(self) -> str:
        """
        Get the player
        """
        return self._player
    
    @property
    def reason(self) -> str:
        """
        Get the reason
        """
        return self._reason


class LocalBlacklisted:
    """
    A class representing a Hypixel Player
    """
    def __init__(self, status: bool, reason: str, blacklist: str) -> None:
        """
        Initialise the class
        
        :param status: Whether the Player is blacklisted or not
        :param reason: The Player blacklist reason
        :param blacklist: The blacklist name
        """
        self._status = status
        self._reason = reason
        self._blacklist = blacklist


    @property
    def status(self) -> bool:
        """
        Get the Player blacklist status
        
        :return: The Player blacklist status
        """
        return self._status

    @property
    def reason(self) -> str:
        """
        Get the Player blacklist reason
        
        :return: The Player blacklist reason
        """
        return self._reason

    @property
    def blacklist(self) -> str:
        """
        Get the blacklist name
        
        :return: The blacklist name
        """
        return self._blacklist


class Blacklist:
    """
    A class representing the overlay local blacklist(s)
    """
    def __init__(self, win) -> None:
        """
        Initialise the class
        
        :param win: The Overlay window
        """
        self.win = win

        self.blacklist: dict[list[PlayerBlacklist]] = {}

        self.loadBlacklist()


    def loadBlacklist(self) -> None:
        """
        Load the local blacklist(s)
        """
        for file in os.listdir(self.win.blacklistConfig):
            if file.endswith(".polsu"):
                filename = file.replace(".polsu", "")

                file_blacklist = []

                try:
                    with open(os.path.join(self.win.blacklistConfig, file), "r") as f:
                        data = f.read().split("\n")

                        for line in data:
                            if ";" in line:
                                player, reason = line.split(";")
                            else:
                                player, reason = line, None

                            if player != "":
                                if "-" in player:
                                    player = player.replace("-", " ")

                                if len(player) > 32 or len(player) < 32 and len(player) > 16:
                                    self.win.logger.warning(f"Invalid player: {player}, skipping...")
                                else:
                                    file_blacklist.append(PlayerBlacklist(player, reason))

                    self.blacklist[filename] = file_blacklist
                except:
                    self.win.logger.warning(f"Invalid blacklist file: {file}, skipping...")


    def getBlacklists(self) -> list[str]:
        """
        Get the local blacklist(s)
        
        :return: The local blacklist(s)
        """
        return list(self.blacklist.keys())
    

    def findPlayer(self, player) -> LocalBlacklisted:
        """
        Find a player in the local blacklist(s)
        
        :param player: The player
        :return: The player data
        """
        for blacklist in self.blacklist:
            for blacklistedPlayer in self.blacklist[blacklist]:
                if blacklistedPlayer.player == player.uuid or blacklistedPlayer.player == player.username  or blacklistedPlayer.player.lower() == player.username.lower():
                    return LocalBlacklisted(
                        status=True,
                        reason=blacklistedPlayer.reason,
                        blacklist=blacklist
                    )

        return LocalBlacklisted(
            status=False,
            reason="",
            blacklist=None
        )


    def addPlayer(self, player: str, reason: str, blacklist: str) -> None:
        """
        Add a player to the local blacklist(s)

        :param player: The player
        :param reason: The reason
        :param blacklist: The blacklist
        """
        if blacklist not in self.blacklist:
            self.blacklist[blacklist] = []

        self.blacklist[blacklist].append(PlayerBlacklist(player, reason))

        self.saveBlacklist(blacklist)


    def removePlayer(self, player: str, blacklist: str) -> None:
        """
        Remove a player from the local blacklist(s)

        :param player: The player
        :param blacklist: The blacklist
        """
        if blacklist in self.blacklist:
            for blacklistedPlayer in self.blacklist[blacklist]:
                if blacklistedPlayer.player == player:
                    self.blacklist[blacklist].remove(blacklistedPlayer)

                    self.saveBlacklist(blacklist)
                    break


    def saveBlacklist(self, blacklist: str) -> None:
        """
        Save the local blacklist(s)

        :param blacklist: The blacklist
        """
        with open(os.path.join(self.win.blacklistConfig, f"{blacklist}.polsu"), "w") as f:
            for player in self.blacklist[blacklist]:
                if player.reason is None:
                    f.write(f"{player.player}\n")
                else:
                    f.write(f"{player.player};{player.reason}\n")
