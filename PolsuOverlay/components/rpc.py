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
from pypresence import Presence as Pr


class Presence:
    """
    RPC - Rich Presence Client
    
    Discord Activity Status.
    """
    def __init__(self, launch):
        self.RPC = Pr(client_id="1076464861921415169")
        self.launch = launch


    def connect(self, player: str = None, stars: str = None, status: str = "Looking to Play..."):
        self.RPC.connect()
        self.update(player, stars, status)


    def clear(self):
        self.RPC.clear()


    def disconnect(self):
        self.clear()
        self.RPC.close()


    def update(self, player: str, stars: str, status: str):
        self.RPC.update(
            buttons=[
                {
                    "label": "Get Overlay 📥", 
                    "url": "https://discord.gg/xm9QX3Q"
                }, 
                {
                    "label": "Discord Server", 
                    "url": "https://discord.gg/xm9QX3Q"
                }
            ],
            large_image="polsu", 
            large_text="Polsu Overlay",

            #small_image="hypixel", 
            #small_text="Playing on Hypixel",

            #details="[376✫] Polsulpicien",
            # "Looking to Play", "Playing Solo", "In a Group"
            #state=status,


            small_image="vscode", 
            small_text="Playing on VSCode",

            details="In Development...",

            start=self.launch
        )
