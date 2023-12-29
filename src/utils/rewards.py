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
import json
import re

from dataclasses import dataclass
from aiohttp import ClientSession


rewardsData = {
    "adsense_token": "Reward Token",
    "housing_package": "Housing Block",
    "specialoccasion_reward_card_skull_green_treasure_chest": "Green Treassure Chest"
}

appdata_regex = re.compile(r"window\.appData = '(.+)';")
csrf_token_regex = re.compile(r"window\.securityToken = \"(.+)\";")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
}


@dataclass(frozen=True)
class Reward:
    rarity: str
    reward_type: str
    amount: int
    game: str
    package: str
    reward_id: int = None
    

    def title(self) -> str:
        """
        Get the title of the reward
        
        :return: The title of the reward
        """
        res = ""

        if self.game:
            if self.game == "Mcgo":
                res += "Cops and Crims"
            else:
                res += f"{self.game} "
        else:
            if self.reward_type == "Souls":
                res += "Skywars "

        if self.package:
            res += f"{self.package}"

        if res == "":
            res = "Hypixel Network"

        return res

    def small(self) -> str:
        """
        Get the small text of the reward
        
        :return: The small text of the reward
        """
        res = ""

        if self.amount > 1:
            res += f"{self.amount}x "

        if self.reward_type:
            if self.reward_type == "Dust":
                res += "Mystery Dust"
            else:
                res += f"{self.reward_type}"

        return res


class Rewards:
    """
    A class that will load and claim rewards from the Hypixel Rewards website (https://rewards.hypixel.net/)
    """
    def __init__(self, url: str) -> None:
        """
        Initialise the Rewards class
        
        :param url: The URL of the reward
        """
        self.url = url

        self.rewards = []


    async def loadRewards(self) -> None:
        """
        Load the rewards
        """
        async with ClientSession(connector=TCPConnector(family=AF_INET6)) as session:
            async with session.get(self.url, headers=headers) as response:
                text = await response.text()
                cookies = response.cookies

        data = appdata_regex.findall(text)
        if data:
            rewardData = json.loads(data[0])
        else:
            raise RuntimeError("Reward expired or was already claimed.")

        if not rewardData.get("rewards"):
            raise RuntimeError("Reward expired or was already claimed.")
        else:
            for index, reward in enumerate(rewardData["rewards"]):
                self.rewards.append(
                    Reward(
                        await self.formatString(reward['rarity']),
                        await self.formatString(reward['reward']),
                        await self.formatString(reward.get('amount', 1)),
                        await self.formatString(reward.get('gameType')),
                        await self.formatString(reward.get("package")),
                        index
                    )
                )

        self.csrf_token = await self.getCsrfToken(text)
        self._csrf = cookies["_csrf"]


    async def claim(self, rewardId: int) -> Reward:
        """
        Claim a reward
        
        :param rewardId: The reward ID
        :return: The reward
        """
        async with ClientSession(cookies={"_csrf": self._csrf}) as session:
            async with session.post(f"https://rewards.hypixel.net/claim-reward/claim?option={self.rewards[rewardId].reward_id}&id={self.url[-8:]}&activeAd=1&_csrf={self.csrf_token}&watchedFallback=false", headers=headers) as response:
                text = await response.text()

                if (text != "reward claimed"):
                    raise RuntimeError("Failed to claim reward")
                else:
                    return self.rewards[rewardId]


    async def getCsrfToken(self, page_string: str) -> str:
        """
        Get the CSRF token
        
        :param page_string: The page string
        :return: The CSRF token
        """
        if csrf_token := csrf_token_regex.findall(page_string):
            return csrf_token[0]

        raise RuntimeError("Could not find CSRF token string")


    async def formatString(self, string: str) -> str:
        """
        Format a string
        
        :param string: The string to format
        :return: The formatted string
        """
        if string in rewardsData:
            string = rewardsData[string]

        if string is None:
            return None
        elif isinstance(string, str):
            return string.replace('_', ' ').capitalize()
        else:
            return string
