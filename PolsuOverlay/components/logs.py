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
from ..utils.rewards import Rewards as Rw
from ..utils.username import isValidPlayer, removeRank

from time import sleep

import re
import keyboard
import asyncio


class Logs:
    """
    A class representing the Log File
    """
    def __init__(self, win) -> None:
        self.win = win

        self.oldString = ""
        self.connected = False
        self.timeIconIndex = 1
        self.error_sent = False

        self.inAParty = False
        
        self.isInGame = False
        self.timerCount = 0

        self.autoWho = False
        self.connecting = False
        self.passThrough = False
        self.queue = []


    def reset(self) -> None:
        """
        Resets the player table
        """
        #for player in self.win.player.threads:
        #    self.win.player.threads[player].terminate()
        
        #for player in self.win.table.skin.threads:
        #    self.win.table.skin.threads[player].terminate()

        #if self.win.configPassThrough and self.passThrough:
        #    self.win.flags(False)

        self.passThrough = False
        self.autoWho = False
        self.queue = []

        self.win.table.resetTable()


    def leftGame(self):
        self.isInGame = False
        self.timerCount = 0


    def who(self) -> None:
        """
        Runs /who
        """
        if self.win.configWho and not self.autoWho:
            self.leftGame()
            self.reset()

            keyboard.press_and_release('t')
            sleep(0.2)
            keyboard.write('/who')
            sleep(0.2)
            keyboard.press_and_release('enter')

            self.autoWho = True


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

        for idx, line in enumerate(lines):
            players = []


            ###############################################
            #                                             #
            #                   EVENTS                    #
            #                                             #
            ###############################################

            # Detects when a player connects to Hypixel
            if "Connecting to mc.hypixel.net" in line:
                self.connecting = True

                self.win.RPC.update("Polsulpicien", 388, "In a lobby")

            # Detects when the client is closed
            elif '[Client thread/INFO]: Stopping!' in line:
                self.leftGame()
                self.reset()

            # If it's the first line after a player connects to Hypixel, the delivery command is executed
            elif self.connecting and "[CHAT] " in line:
                sleep(0.4)
                keyboard.press_and_release('t')
                sleep(0.2)
                keyboard.write('/delivery')
                sleep(0.2)
                keyboard.press_and_release('enter')

                self.connecting = False

            # Detects a reward link in the chat and loads the rewards
            elif "Click the link to visit our website and claim your reward: " in line \
            or "To choose your reward you have to click the link to visit our website! As a reminder, here's your link for today:  " in line:
                self.win.reward = Rw(line.split(': ')[1].split('\n')[0].replace('\n', '').replace(' ', ''))
                asyncio.run(self.win.reward.loadRewards())

                if not self.win._rewardsOpened and self.win.height() >= 220:
                    self.win.openRewards()
                    self.win.rewards.updateWindow()

                self.win.notif.send(
                    title="Hypixel Daily Delivery Reward",
                    message="You can claim your reward."
                )

            # Detects when a game starts
            elif "The game starts in 1 second!" in line:
                self.isInGame = True

                # if self.win.configPassThrough:
                #    self.passThrough = True
                #    self.win.flags(True)

            # Detects when the player changes server
            # The second string is to avoid castle streaks messages (e.g. wither)
            elif "Sending you to" in line or "[Client thread/INFO]: [CHAT]                                      " \
            in line and not "                                                                              " in line:
                self.leftGame()
                self.reset()

            elif "[CHAT]        " in line and not "[CHAT]        " in lines[idx-1] and not "[CHAT]        " in lines[idx+1] \
                and not "[CHAT]                          " in line and not "[CHAT]              Select an Option or Sneak to Cancel." in line:
                self.who()

            # Detects when a player joins a started game
            elif "To leave " in line:
                self.who()


            ###############################################
            #                                             #
            #                  COMMANDS                   #
            #                                             #
            ###############################################

            # Detects when /who is executed
            elif "ONLINE: " in line:
                self.reset()

                players.extend(line.split("ONLINE: ")[1].split(', '))
                self.autoWho = True

            # Detects when /list is executed
            elif "Online Players (" in line:
                p = line.split("): ")[1].split(', ')

                for i in range(0, len(p)):
                    x = p[i].split(' ')

                    if len(x) > 1:
                        players.append(x[1])
                    else:
                        players.append(x[0])

            # Detects when /msg +PLAYER is executed
            elif "Can't find a player by the name of '+" in line:
                player = line.split("Can't find a player by the name of '+")[1].replace("'", "")
                if isValidPlayer(player):
                    self.queue.append(player)
                    self.win.player.getPlayer([player])


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

            # Detects when you join a party, loads the party leader
            elif "You have joined " in line and "'s party!" in line:
                # You have joined [MVP+] egdo's party!
                # You'll be partying with: [VIP+] Polsulpicien

                player = line.split("You have joined ")[1].split("'s party!")[0]
                players.append(removeRank(player))

            # Loads the party members when you join a party
            elif "You'll be partying with: " in line:
                # You'll be partying with: [MVP+] egdo

                p = line.split("You'll be partying with: ")[1].split(", ")

                for player in p:
                    players.append(removeRank(player))

            # When a player is removed from the party
            elif " was removed" in line:
                # [MVP+] egdo was removed from the party

                player = line.split(" was removed")[0].split(" ")[4]

                self.queue.remove(player)
                self.win.table.removePlayerFromName(player)

            # When a player leaves the party
            elif " has left the party." in line:
                # [MVP+] egdo has left the party.

                player = line.split(" has left the party.")[0].split(" ")[4]

                self.queue.remove(player)
                self.win.table.removePlayerFromName(player)

            # Detects when /party list is executed, loads the party leader
            elif "Party Leader: " in line:
                # Party Leader: [VIP+] Polsulpicien

                player = line.split("Party Leader: ")[1]
                players.append(removeRank(player))

            # Detects when /party list is executed, loads the party moderators
            elif "Party Moderators: " in line:
                # Party Moderators: [MVP+] _lior

                p = line.split("Party Moderators: ")[1].split(", ")

                for player in p:
                    players.append(removeRank(player))

            # Detects when /party list is executed, loads the party members
            elif "Party Members: " in line:
                # Party Members: [MVP+] egdo

                p = line.split("Party Members: ")[1].split(" ? ")

                for player in p:
                    players.append(removeRank(player))


            ###############################################
            #                                             #
            #                   LOBBY                     #
            #                                             #
            ###############################################

            # Detects when a player joins the lobby
            elif " has joined (" in line:
                self.who()

                player = line.split(" has joined (")[0].split(' '[0])[-1]
                players.append(removeRank(player))

            # Detects when a player leaves the lobby
            elif " has quit!" in line:
                player = line.split(" has quit!")[0].split(" ")[4]

                self.queue.remove(player)
                self.win.table.removePlayerFromName(player)


            # If some players where detected, add them to the queue
            if players:
                self.queue.extend(players)
                self.win.player.getPlayer(players)
