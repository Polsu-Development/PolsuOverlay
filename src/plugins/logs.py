from ..components.logs import Logs


class PluginLogs:
    def __init__(self, logs: Logs) -> None:
        self.reset = logs.reset
        self.isConnecting = logs.isConnecting
        self.inGame = logs.inGame
        self.isWaitingForGame = logs.isWaitingForGame
        self.isInAParty = logs.isInAParty
        self.getPartyMembers = logs.getPartyMembers
        