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
from .. import __version__


import asyncio
import traceback

from pypresence import Presence as Pr, DiscordNotFound
from threading import Thread


def startRPC(win) -> None:
    """
    Start the Discord RPC
    
    :param win: The Overlay window
    """
    win.logger.debug("Starting Discord RPC Thread...")
    Thread(target=discordRPC, args=(win, asyncio.new_event_loop(), ), daemon=True).start()


def discordRPC(win, loop) -> None:
    """
    Discord RPC
    
    :param win: The Overlay window
    :param loop: The asyncio event loop
    """
    asyncio.set_event_loop(loop)

    try:
        win.RPC = Presence(win.launch, win.logs, win.configStatus)
        win.RPC.connect()

        win.logger.info("Discord RPC connected!")

        #self.notif.send(
        #    title="Discord Activity Status Update",
        #    message="Succesfully connected to Discord!"
        #)
    except DiscordNotFound:
        win.RPC = None

        win.logger.debug("Could not find Discord installed and running on this machine.")
    except:
        win.RPC = None

        win.logger.error(f"Discord RPC Error.\n\nTraceback: {traceback.format_exc()}")

        #self.notif.send(
        #    title="Discord Activity Status Error",
        #    message="Something went wrong, are you sure that your Discord client is opened?"
        #)


class Presence:
    """
    RPC - Rich Presence Client
    
    Discord Activity Status.
    """
    def __init__(self, launch: int, logs, configStatus: bool) -> None:
        """
        Initialise the Discord RPC
        
        :param launch: The time when the overlay was launched
        :param logs: The logs
        :param configStatus: The config status
        """
        self.RPC = Pr(client_id="1076464861921415169")
        self.launch = launch
        self.logs = logs
        self.configStatus = configStatus

        self.player = None


    def connect(self) -> None:
        """
        Connect to Discord
        """
        self.RPC.connect()
        self.update()

    
    def setPlayer(self, player) -> None:
        """
        Set the player
        """
        self.player = player
        self.update()


    def setConfigStatus(self, status: bool) -> None:
        """
        Set the config status
        
        :param status: The config status
        """
        self.configStatus = status
        self.update()


    def clear(self) -> None:
        """
        Clear the RPC
        """
        self.RPC.clear()


    def disconnect(self) -> None:
        """
        Disconnect from Discord
        """
        self.clear()
        self.RPC.close()


    def update(self) -> None:
        """
        Update the RPC
        """
        elapsed = self.launch

        if self.configStatus:
            if self.player:
                details = f"[{self.player.bedwars.stars}✫] {self.logs.rawLine(self.player.rank)}"
            else:
                details = None

            party = None
            if self.logs.party:
                state = "In a Bedwars Party!"
                party = [self.logs.partyMembers, self.logs.partyMembers]
                if self.logs.isInGame:
                    small_image = "bedwars"

                    elapsed = int(self.logs.gameStart.timestamp())
                else:
                    small_image = "hypixel"
            elif self.logs.waitingForGame:
                state = "Waiting for the game to start..."
                small_image = "bedwars"
            elif self.logs.isInGame:
                state = "In a Bedwars Game!"
                small_image = "bedwars"

                elapsed = int(self.logs.gameStart.timestamp())
            else:
                state = "Looking to Play..."
                small_image = "hypixel"
        else:
            details = None
            state = None
            small_image = "hypixel"
            party = None

        try:
            self.RPC.update(
                state=state,
                details=details,
                start=elapsed,
                large_image="polsu", 
                large_text=f"Polsu Overlay v{__version__}",
                small_image=small_image, 
                small_text="Playing on mc.hypixel.net",
                party_size=party,
                buttons=[
                    {
                        "label": "Get Overlay 📥", 
                        "url": "https://discord.polsu.xyz" # TODO: overlay.polsu.xyz
                    }, 
                    {
                        "label": "Discord Server", 
                        "url": "https://discord.polsu.xyz"
                    }
                ],
            )
        except AssertionError:
            # You must connect your client before sending events!
            pass
