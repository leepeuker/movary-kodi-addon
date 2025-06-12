import xbmc
import xbmcaddon
import urllib.request
import json

class MovaryPlayer(xbmc.Player):
    def __init__(self):
        super().__init__()
        self.current_movie = None
        self.webhook_url = None
        self.is_enabled = None
        self.load_settings()

    def load_settings(self):
        self.webhook_url = xbmcaddon.Addon().getSetting("movary.webhook.url")
        self.is_enabled = xbmcaddon.Addon().getSetting("movary.is_enabled") == "true"
        xbmc.log(f"Movary: Reloaded addon settings", level=xbmc.LOGINFO)

    def onAVStarted(self):
        if not self.is_enabled:
            return
        xbmc.log(f"Movary: Play started", level=xbmc.LOGINFO)
        self.getCurrentMovieInfo()

    def onPlayBackPaused(self):
        if not self.is_enabled or not self.current_movie:
            return
        xbmc.log(f"Movary: Play paused", level=xbmc.LOGINFO)

    def onPlayBackResumed(self):
        if not self.is_enabled or not self.current_movie:
            return
        xbmc.log(f"Movary: Play resumed", level=xbmc.LOGINFO)

    def onPlayBackStopped(self):
        if not self.is_enabled or not self.current_movie:
            return
        xbmc.log(f"Movary: Play stopped", level=xbmc.LOGINFO)
        self.sendWebhookRequest()

    def onPlayBackEnded(self):
        if not self.is_enabled or not self.current_movie:
            return
        xbmc.log(f"Movary: Play ended", level=xbmc.LOGINFO)

    def getCurrentMovieInfo(self):
        if not self.isPlayingVideo():
            xbmc.log(f"Movary: Play ignored: play is no movie", level=xbmc.LOGINFO)
            self.current_movie = None
            return

        tag = self.getVideoInfoTag()
        if not tag:
            xbmc.log(f"Movary: Play ignored: no video info tag", level=xbmc.LOGINFO)
            self.current_movie = None
            return

        if tag.getMediaType() != "movie":
            xbmc.log(f"Movary: Play ignored: play is no movie", level=xbmc.LOGINFO)
            self.current_movie = None
            return

        tmdb_id = xbmc.getInfoLabel("VideoPlayer.UniqueID(tmdb)")

        self.current_movie = {
            "title": tag.getTitle(),
            "year": tag.getYear(),
            "tmdb_id": tmdb_id if tmdb_id else None,
        }

        xbmc.log(f"Movary: Detected playing movie: {self.current_movie}", level=xbmc.LOGINFO)

    def sendWebhookRequest(self, tmdb_id):
        if not self.current_movie.tmdb_id:
            xbmc.log(f"Movary: Did not send played movie webhook. Movie has no tmdb id: {self.current_movie}", level=xbmc.LOGINFO)
            return

        payload = {
            "uniqueIds": {
                "tmdbId" : self.current_movie.tmdb_id
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
            xbmc.log(f"Movary: Sending played movie webhook request with payload: {payload}", level=xbmc.LOGINFO)

            request = urllib.request.Request(
                url=self.webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers
            )
            with urllib.request.urlopen(request) as response:
                xbmc.log(f"Movary: Played movie webhook request sent. Response code: {response.status}", level=xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f"Movary: Played movie webhook request failed to sent: {e}", level=xbmc.LOGERROR)