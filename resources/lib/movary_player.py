import xbmc
import xbmcaddon
import urllib.request
import json

class MovaryPlayer(xbmc.Player):
    def __init__(self):
        super().__init__()
        xbmc.log("Movary: Settings changed, reloading...", level=xbmc.LOGINFO)
        self.webhook_url = None
        self.is_enabled = None
        self.load_settings()

    def load_settings(self):
        self.webhook_url = xbmcaddon.Addon().getSetting("movary.webhook.url")
        self.is_enabled = xbmcaddon.Addon().getSetting("movary.is_enabled")
        xbmc.log(f"Movary: Reloaded addon settings", level=xbmc.LOGINFO)

    def onAVStarted(self):
        if not self.is_enabled:
            return
        xbmc.log(f"Movary: Play started", level=xbmc.LOGINFO)

    def onPlayBackPaused(self):
        if not self.is_enabled:
            return
        xbmc.log(f"Movary: Play paused", level=xbmc.LOGINFO)

    def onPlayBackResumed(self):
        if not self.is_enabled:
            return
        xbmc.log(f"Movary: Play resumed", level=xbmc.LOGINFO)

    def onPlayBackStopped(self):
        if not self.is_enabled:
            return
        xbmc.log(f"Movary: Play stopped", level=xbmc.LOGINFO)
        # TODO: get the tmdbId of the current item
        # self.send_webhook_request(tmdbId)

    def onPlayBackEnded(self):
        if not self.is_enabled:
            return
        xbmc.log(f"Movary: Play ended", level=xbmc.LOGINFO)

    def send_webhook_request(self, tmdb_id):
        payload = {
            "uniqueIds": {
                "tmdbId" : tmdb_id
            },
        }
        headers = {'Content-Type': 'application/json'}

        if not self.is_enabled:
            xbmc.log(f"Movary: Did not send played movie webhook. Addon not enabled.", level=xbmc.LOGINFO)
            return

        if not self.webhook_url:
            xbmc.log(f"Movary: Did not send played movie webhook. Webhook URL not set.", level=xbmc.LOGERROR)
            return

        try:
            request = urllib.request.Request(
                url=self.webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers
            )
            with urllib.request.urlopen(request) as response:
                xbmc.log(f"Movary: Played movie webhook request sent. Response code: {response.status}", level=xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f"Movary: Played movie webhook request failed to sent: {e}", level=xbmc.LOGERROR)