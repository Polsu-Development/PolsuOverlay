from ..components.notifications import Notif


class PluginNotification:
    def __init__(self, notification: Notif) -> None:
        self.send = notification.send
