import xbmc
import xbmcaddon
import urllib.request
import json

class MovaryMonitor(xbmc.Monitor):
    def __init__(self):
        super().__init__()
        self.addon = xbmcaddon.Addon()
        self.webhook_url = None
        self.load_settings()

    def onSettingsChanged(self):
        xbmc.log("Movary: Settings changed, reloading...", level=xbmc.LOGINFO)
        self.load_settings()

    def load_settings(self):
        self.webhook_url = self.addon.getSetting("movary.webhook.url")
        xbmc.log(f"Movary: Reloaded webhook url '{self.webhook_url}'", level=xbmc.LOGINFO)

    def send_webhook_request(self):
        payload = {
            "uniqueIds": {
                "tmdbId" : None
            },
        }
        headers = {'Content-Type': 'application/json'}

        if not self.webhook_url:
            xbmc.log(f"Movary: Failed to send webhook. Webhook URL not set.", level=xbmc.LOGERROR)
            return

        try:
            request = urllib.request.Request(
                url=self.webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers
            )
            with urllib.request.urlopen(request) as response:
                xbmc.log(f"Movary: Webhook request sent. Response code: {response.status}", level=xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f"Movary: Failed to send webhook: {e}", level=xbmc.LOGERROR)