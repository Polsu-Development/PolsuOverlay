from dataclasses import dataclass
import requests
import json
import re


# Don't know all the data yet
rewardsData = {
    "adsense_token": "Reward Token",
    "housing_package": "Housing Block",
    "specialoccasion_reward_card_skull_green_treasure_chest": "Green Treassure Chest"
}

appdata_regex = re.compile(r"window\.appData = '(.+)';")
csrf_token_regex = re.compile(r"window\.securityToken = \"(.+)\";")
reward_id_regex = re.compile(r"(https?://)?rewards.hypixel.net/claim-reward/(.{8})/?")
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

        return res

    def small(self) -> str:
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
    def __init__(self, url):
        self.url = url

        self.session = requests.session()


    async def loadRewards(self):
        r = self.session.get(self.url, headers=headers)

        data = re.compile(r"window\.appData = '(.+)';").findall(r.text)
        if data:
            rewardData = json.loads(data[0])
        else:
            raise RuntimeError("Reward expired or was already claimed.")

        if not rewardData.get("rewards"):
            raise RuntimeError("Reward expired or was already claimed.")
        else:
            self.rewards = []
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

        self.csrf_token = await self.getCsrfToken(r.text)
        self._csrf = r.cookies["_csrf"]


    async def claim(self, rewardId):
        reward_id = self.url[-8:]
        r = requests.post("https://rewards.hypixel.net/claim-reward/claim", params={
            "option": self.rewards[rewardId].reward_id,
            "id": reward_id,
            "activeAd": 1,
            "_csrf": self.csrf_token,
            "watchedFallback": "false",
        }, cookies={"_csrf": self._csrf}, headers=headers)

        if (r.text != "reward claimed"):
            raise RuntimeError("Failed to claim reward")


    async def getCsrfToken(self, page_string: str) -> str:
        if csrf_token := csrf_token_regex.findall(page_string):
            return csrf_token[0]

        raise RuntimeError("Could not find CSRF token string")


    async def formatString(self, string: str):
        if string in rewardsData:
            string = rewardsData[string]

        if string is None:
            return None
        elif isinstance(string, str):
            return string.replace('_', ' ').capitalize()
        else:
            return string
