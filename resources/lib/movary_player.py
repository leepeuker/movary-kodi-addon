import xbmc
import xbmcaddon
import urllib.request
import json

class MovaryPlayer(xbmc.Player):
    def __init__(self):
        super().__init__()
        xbmc.log("Movary: Settings changed, reloading...", level=xbmc.LOGINFO)
        self.webhook_url = None
        self.load_settings()

    def load_settings(self):
        self.webhook_url = xbmcaddon.Addon().getSetting("movary.webhook.url")
        xbmc.log(f"Movary: Reloaded webhook url '{self.webhook_url}'", level=xbmc.LOGINFO)

    def onAVStarted(self):
        xbmc.log(f"Movary: Play started", level=xbmc.LOGINFO)

    def onPlayBackPaused(self):
        xbmc.log(f"Movary: Play paused", level=xbmc.LOGINFO)

    def onPlayBackResumed(self):
        xbmc.log(f"Movary: Play resumed", level=xbmc.LOGINFO)

    def onPlayBackStopped(self):
        xbmc.log(f"Movary: Play stopped", level=xbmc.LOGINFO)

    def onPlayBackEnded(self):
        xbmc.log(f"Movary: Play ended", level=xbmc.LOGINFO)

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