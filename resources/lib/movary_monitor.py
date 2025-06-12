import xbmc
import xbmcaddon

class MovaryMonitor(xbmc.Monitor):
    def __init__(self):
        super().__init__()
        self.addon = xbmcaddon.Addon()
        self.settings = None
        self.load_settings()

    def onSettingsChanged(self):
        self.load_settings()

    def load_settings(self):
        self.settings = addon.getSettings()

        xbmc.log("Movary: Loaded webhook url '" + self.settings.getString("movary.webhook.url") + "'", level=xbmc.LOGINFO)
