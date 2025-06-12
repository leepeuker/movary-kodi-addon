import xbmc

from resources.lib.player_monitor import PlayerMonitor

class MovaryMonitor(xbmc.Monitor):
    def __init__(self):
        super().__init__()

        self.movary_player = MovaryPlayer()

    def onSettingsChanged(self):
        self.movary_player.load_settings()

    def send_webhook_request(self):
        self.movary_player.send_webhook_request()
