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
from .reward import openRewards
from ..utils.rewards import Rewards as Rw
from ..utils.username import isValidPlayer, removeRank
from ..utils.constants import PLAYER_MESSAGE_PATTERN, CLIENT_NAMES

from time import sleep
from datetime import datetime

import re
from pynput.keyboard import Key, Controller
import asyncio
import traceback
import pywinctl


def get_active_window_title():
    active_window = pywinctl.getActiveWindow()
    return active_window.title if active_window else None


class Logs:
    """
    A class representing the Log File
    """
    def __init__(self, win) -> None:
        """
        Initialise the Logs class

        :param win: The Overlay window
        """
        self.win = win

        self.oldString = ""
        self.timeIconIndex = 1
        self.error_sent = False

        self.waitingForGame = False
        self.isInGame = False
        self.gameStart = None

        self.party = False
        self.partyMembers = 1

        self.autoWho = False
        self.connecting = False
        self.hideOverlay = False
        self.hideOverlayTimer = 0
        self.queue = []

        self.keyboard = Controller()

    
    def isConnecting(self) -> bool:
        """
        Returns if the player is connecting to Hypixel
        
        :return: A boolean representing if the player is connecting to Hypixel
        """
        return self.connecting


    def inGame(self) -> bool:
        """
        Returns if the player is in a game

        :return: A boolean representing if the player is in a game
        """
        return self.isInGame


    def isWaitingForGame(self) -> bool:
        """
        Returns if the player is waiting for a game

        :return: A boolean representing if the player is waiting for a game
        """
        return self.waitingForGame


    def isInAParty(self) -> bool:
        """
        Returns if the player is in a party

        :return: A boolean representing if the player is in a party
        """
        return self.party
    

    def getPartyMembers(self) -> int:
        """
        Returns the number of party members

        :return: An integer representing the number of party members
        """
        return self.partyMembers
    

    def reset(self, autowho: bool = False) -> None:
        """
        Resets the player table

        :param autowho: A boolean representing if the /who
        """
        self.hideOverlay = False
        self.hideOverlayTimer = 0
        self.autoWho = autowho
        self.queue = []

        self.win.table.resetTable()


    def leftGame(self) -> None:
        """
        Resets the game variables
        """
        self.isInGame = False
        self.gameStart = None
        self.waitingForGame = False
        self.hideOverlay = False
        self.hideOverlayTimer = 0


    def who(self) -> None:
        """
        Runs /who
        """
        if not self.autoWho:
            self.leftGame()
            self.reset()

            if self.win.configWho:
                active = get_active_window_title()
                if any(client in active for client in CLIENT_NAMES):
                    self.keyboard.press('t')
                    self.keyboard.release('t')
                    sleep(0.2)
                    self.keyboard.type('/who')
                    sleep(0.2)
                    self.keyboard.press(Key.enter)
                    self.keyboard.release(Key.enter)
                else:
                    self.autoWho = False
                
                self.waitingForGame = True


    def task(self) -> None:
        """
        The main task which reads the log file
        """
        if self.oldString == "":
            self.readLogFile()
        else:
            try:
                self.readLogs()
            except:
                self.win.logger.error(f"Error while reading logs.\n\nTraceback: {traceback.format_exc()}")


    def readLogFile(self) -> str:
        """
        Function which returns the new lines of the log file

        :return: A string containing the new lines of the log file
        """
        try:
            with open(self.win.configLogPath, "r+") as logFile:
                contents = logFile.read()

            new = contents[len(self.oldString):]
            self.oldString = contents

            self.error_sent = False

            return new
        except FileNotFoundError:
            if not self.error_sent:
                self.win.notif.send(
                    title="Warning!",
                    message="The log file you are currently using isn't valid.\nGo to: Settings -> Client, and choose a valid client.",
                    block=True
                )

                # To avoid multiple notifications
                self.error_sent = True
            return ""
        except:
            return ""


    def rawLine(self, string: str) -> str:
        """
        Format a line, removes colour codes and special characters such as stars

        :param string: A string representing a line
        :return: A string representing the cleaned line
        """
        invalidChars1 = re.findall(r"[✫✪⚝]", string)
        for char in invalidChars1:
            string = string.replace(char, "")

        invalidChars2 = re.findall(r"§|¡±", string)
        for char in invalidChars2:
            string = string.replace(char, "�")

        string = re.sub(r"(?i)�[0-9A-FK-OR]", "", string)
        return string


    def readLogs(self) -> None:
        """
        Function which detected players in the new lines added in the log file
        Automatically add them to the queue, to get their stats and display them on the overlay
        """
        line: str = self.readLogFile()
        lines = self.rawLine(line).splitlines()

        for l in lines:
            line = l.replace(" [System] ", "")

            if "[Client thread/INFO]: " in line:
                lines = line.split("[Client thread/INFO]: ")
                if len(lines) >= 1:
                    line = lines[1]

            players = []

            if PLAYER_MESSAGE_PATTERN.findall(line.replace("[CHAT] ", "")):
                self.win.plugins.broadcast("on_player_message", line.replace("[CHAT] ", ""))
                return


            ###############################################
            #                                             #
            #                   EVENTS                    #
            #                                             #
            ###############################################

            # Detects when a player connects to Hypixel
            if "Connecting to mc.hypixel.net" in line:
                self.connecting = True

            # Detects when the client is closed
            elif '[Client thread/INFO]: Stopping!' in line:
                self.leftGame()
                self.reset()

            # If it's the first line after a player connects to Hypixel, the delivery command is executed
            elif self.connecting and "[CHAT] " in line:
                active = get_active_window_title()
                if any(client in active for client in CLIENT_NAMES):
                    sleep(0.5)
                    self.keyboard.press('t')
                    self.keyboard.release('t')
                    sleep(0.3)
                    self.keyboard.type('/delivery')
                    sleep(0.3)
                    self.keyboard.press(Key.enter)
                    self.keyboard.release(Key.enter)

                self.connecting = False

            # Detects a reward link in the chat and loads the rewards
            elif "Click the link to visit our website and claim your reward: " in line \
            or "To choose your reward you have to click the link to visit our website! As a reminder, here's your link for today:  " in line:
                self.win.reward = Rw(line.split(': ')[1].split('\n')[0].replace('\n', '').replace(' ', ''))
                asyncio.run(self.win.reward.loadRewards())

                if not self.win._rewardsOpened and self.win.height() >= 220:
                    openRewards(self.win)
                    self.win.rewards.updateWindow()

                self.win.notif.send(
                    title="Hypixel Daily Delivery Reward",
                    message="You can claim your reward."
                )

            # Detects when a game starts
            elif "The game starts in 1 second!" in line:
                self.waitingForGame = False
                self.isInGame = True
                self.gameStart = datetime.now()

                if self.win.confighideOverlay:
                    self.hideOverlay = True
                    self.hideOverlayTimer = 0

                self.win.plugins.broadcast("on_game_start")

            elif "[CHAT] You have been eliminated!" == line:
                self.hideOverlay = False
                self.hideOverlayTimer = 0

                self.win.plugins.broadcast("on_final_death")

            # Detects when a player joins a started game
            elif line.startswith("To leave ") or "[CHAT]        " == line:
                self.leftGame()
                self.reset()
                self.who()

            # Detects when the player changes server
            elif "[CHAT]                                      " ==  line or line.startswith("Found an in-progress") or line.startswith("Sending you to"):
                self.leftGame()
                self.reset()


            ###############################################
            #                                             #
            #                  COMMANDS                   #
            #                                             #
            ###############################################

            # Detects when /who is executed
            elif line.startswith("[CHAT] ONLINE: "):
                self.reset()

                players.extend(line.split("ONLINE: ")[1].split(', '))
                self.queue = players

                self.autoWho = True

                self.win.player.getPlayer(players)
                self.win.plugins.broadcast("on_who", players)
                players = []

            # Detects when /list is executed
            elif line.startswith("[CHAT] Online Players ("):
                p = line.split("): ")[1].split(', ')

                for i in range(0, len(p)):
                    x = p[i].split(' ')

                    if len(x) > 1:
                        players.append(x[1])
                    else:
                        players.append(x[0])

                self.win.plugins.broadcast("on_list", players)

            # Detects when /msg +PLAYER is executed
            elif "Can't find a player by the name of '+" in line:
                player = line.split("Can't find a player by the name of '+")[1].replace("'", "")
                if isValidPlayer(player):
                    players.append(player)


            ###############################################
            #                                             #
            #                   PARTY                     #
            #                                             #
            ###############################################

            # Detects when the party leader invites a player
            elif " to the party! They have 60 seconds to accept" in line:
                # [VIP+] Polsulpicien invited [MVP+] egdo to the party!
                # They have 60 seconds to accept.

                player = line.split('invited ')[1].split(' to the party! They have 60 seconds to accept')[0]
                players.append(removeRank(player))

            # Detects when someone invites you to their party
            elif " has invited you to join their party!" in line:
                # [VIP+] Polsulpicien has invited you to join their party!

                player = line.split(' has')[0].split(' ')[-1]
                players.append(removeRank(player))

            # Detects when a player joins a party
            elif " joined the party." in line:
                # [VIP+] Polsulpicien joined the party.

                player = line.split(" joined the party.")[0].split("[CHAT] ")[1]
                players.append(removeRank(player))

                self.party = True
                self.partyMembers += 1

            # Detects when you join a party, loads the party leader
            elif "You have joined " in line and "'s party!" in line:
                # You have joined [MVP+] egdo's party!
                # You'll be partying with: [VIP+] Polsulpicien

                player = line.split("You have joined ")[1].split("'s party!")[0]
                players.append(removeRank(player))

                self.party = True

            # Loads the party members when you join a party
            elif "You'll be partying with: " in line:
                # You'll be partying with: [MVP+] egdo

                p = line.split("You'll be partying with: ")[1].split(", ")

                for player in p:
                    players.append(removeRank(player))

                self.party = True
                self.partyMembers = len(p)

            # When a player is removed from the party
            elif " was removed from the party." in line:
                # [MVP+] egdo was removed from the party

                try:
                    player = line.split(" was removed from the party.")[0].split(" ")[4]
                except:
                    self.win.logger.error(f"Error while removing a player.\n\nTraceback: {traceback.format_exc()}")

                self.win.table.removePlayerFromName(player)

                self.partyMembers -= 1

            # When a player leaves the party
            elif " has left the party." in line:
                # [MVP+] egdo has left the party.

                player = line.split(" has left the party.")[0].split(" ")[1]

                self.win.table.removePlayerFromName(player)

                self.partyMembers -= 1

            elif " has been removed from the party." in line:
                # [MVP+] egdo has been removed from the party.

                player = line.split("[CHAT] ")[1].split(" has been removed from the party.")[0]

                self.win.table.removePlayerFromName(player)

                self.partyMembers -= 1

            # Detect when you leave the party
            elif line == "[CHAT] You left the party.":
                # You left the party.

                self.party = False
                self.partyMembers = 1

            # Detects when the party is disbanded
            elif line == "[CHAT] The party was disbanded because all invites expired and the party was empty.":
                # The party was disbanded because all invites expired and the party was empty.

                self.party = False
                self.partyMembers = 1

            # Dectects when you are kicked from the party
            elif line.startswith("[CHAT] You have been kicked from the party by"):
                # You have been kicked from the party by [MVP] Polsulpicien

                self.party = False
                self.partyMembers = 1

            # Detects when /party list is executed, loads the party leader
            elif "Party Leader: " in line:
                # Party Leader: [VIP+] Polsulpicien

                player = line.split("Party Leader: ")[1]
                players.append(removeRank(player))

                self.party = True
                self.partyMembers = 1

            # Detects when /party list is executed, loads the party moderators
            elif "Party Moderators: " in line:
                # Party Moderators: [MVP+] _lior

                p = line.split("Party Moderators: ")[1].split(", ")

                for player in p:
                    if player != "":
                        self.partyMembers += 1
                        players.append(removeRank(player))


            # Detects when /party list is executed, loads the party members
            elif "Party Members: " in line:
                # Party Members: [MVP+] egdo

                p = line.split("Party Members: ")[1].split(" ? ")

                for player in p:
                    if player != "":
                        self.partyMembers += 1
                        players.append(removeRank(player))


            # If some players where detected, add them to the queue
            if players:
                self.win.player.getPlayer(players, True)
                players = []


            ###############################################
            #                                             #
            #                   LOBBY                     #
            #                                             #
            ###############################################

            # Detects when a player joins the lobby
            if " has joined (" in line:
                self.who()

                player = line.split(" has joined (")[0].split(' '[0])[-1]
                self.queue.append(player)
                players.append(removeRank(player))

                self.win.plugins.broadcast("on_join", player)

            # Detects when a player leaves the lobby
            elif " has quit!" in line:
                player = line.split("[CHAT] ")[1].split(" has quit!")[0]

                if player in self.queue:
                    self.queue.remove(player)
                    self.win.table.removePlayerFromName(player)

                self.win.plugins.broadcast("on_quit", player)

            elif line.endswith("FINAL KILL!"):
                player = line.replace("[CHAT] ", "").split(" ")[0]
                
                if player in self.queue:
                    self.queue.remove(player)
                    self.win.table.removePlayerFromName(player)

                self.win.plugins.broadcast("on_final_kill", player)


            # If some players where detected, add them to the queue
            if players:
                self.win.player.getPlayer(players)


            self.win.plugins.broadcast("on_message", line)
