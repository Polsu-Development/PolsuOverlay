from ..components.table import Table


class PluginTable:
    def __init__(self, table: Table) -> None:
        self.insert = table.insert
        self.update = table.update
        self.resetTable = table.resetTable
        self.removePlayerFromUUID = table.removePlayerFromUUID
        self.removePlayerFromName = table.removePlayerFromName
        self.getPlayers = table.getPlayers
        self.getUUIDs = table.getUUIDs
        self.updateHeaders = table.updateHeaders
        self.getHeaders = table.getHeaders
        self.sort = table.sort
