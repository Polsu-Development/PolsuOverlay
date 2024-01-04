from ..components.blacklist import Blacklist


class PluginBlacklist:
    def __init__(self, blacklist: Blacklist) -> None:
        self.blacklist = blacklist.blacklist
        self.getBlacklists = blacklist.getBlacklists
        self.findPlayer = blacklist.findPlayer
        self.addPlayer = blacklist.addPlayer
        self.removePlayer = blacklist.removePlayer
