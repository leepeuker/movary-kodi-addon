import xbmc

from resources.lib.movary_player import MovaryPlayer

class MovaryMonitor(xbmc.Monitor):
    def __init__(self):
        super().__init__()

        self.movary_player = MovaryPlayer()

    def onSettingsChanged(self):
        self.movary_player.load_settings()
