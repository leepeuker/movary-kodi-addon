import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import urllib.request
import json
import threading

class MovaryPlayer(xbmc.Player):
    def __init__(self, *args):
        super().__init__()
        self.current_movie = None
        self.webhook_url = None
        self.is_enabled = None
        self.load_settings()
        self.watch_timer = None
        self.watch_timer_active = False
        self.watch_timer_paused = False
        self.current_runtime_position = None

    def load_settings(self):
        self.webhook_url = xbmcaddon.Addon().getSetting("movary.webhook.url")
        self.is_enabled = xbmcaddon.Addon().getSetting("movary.is_enabled") == "true"
        xbmc.log(f"Movary: Reloaded addon settings", level=xbmc.LOGINFO)

    def show_message(self, message: str, duration: int = 5000):
        addon = xbmcaddon.Addon()
        icon_path = xbmcvfs.translatePath(addon.getAddonInfo("path") + "/resources/icon.png")
        dialog = xbmcgui.Dialog()
        dialog.notification("Movary", message, icon=icon_path, time=duration)

    def startWatchTimer(self):
        self.watch_timer_active = True

        def update_current_runtime_position():
            while self.watch_timer_active and self.isPlaying():
                if not self.watch_timer_paused:
                    try:
                        self.current_runtime_position = self.getTime()
                        xbmc.log("Movary: Watch timer updated current runtime positon", level=xbmc.LOGDEBUG)
                    except Exception:
                        xbmc.log("Movary: Failed to get time", level=xbmc.LOGWARNING)
                xbmc.sleep(10000)  # 10 seconds

        self.watch_timer = threading.Thread(target=update_current_runtime_position)
        self.watch_timer.daemon = True
        self.watch_timer.start()

    def stopWatchTimer(self):
        self.watch_timer_active = False
        if self.watch_timer is not None:
            self.watch_timer.join(timeout=1)
            self.watch_timer = None
        xbmc.log("Movary: Watch timer stopped", level=xbmc.LOGDEBUG)

    def pauseWatchTimer(self):
        self.watch_timer_paused = True
        xbmc.log("Movary: Watch timer paused", level=xbmc.LOGDEBUG)

    def resumeWatchTimer(self):
        self.watch_timer_paused = False
        xbmc.log("Movary: Watch timer resumed", level=xbmc.LOGDEBUG)

    def onAVStarted(self):
        if not self.is_enabled:
            return
        xbmc.log(f"Movary: Play started", level=xbmc.LOGDEBUG)
        self.getCurrentMovieInfo()
        self.startWatchTimer()

    def onPlayBackPaused(self):
        if not self.is_enabled or not self.current_movie:
            return
        xbmc.log(f"Movary: Play paused", level=xbmc.LOGDEBUG)
        self.pauseWatchTimer()

    def onPlayBackResumed(self):
        if not self.is_enabled or not self.current_movie:
            return
        xbmc.log(f"Movary: Play resumed", level=xbmc.LOGDEBUG)
        self.resumeWatchTimer()

    def onPlayBackStopped(self):
        if not self.is_enabled or not self.current_movie:
            return
        self.stopWatchTimer()

        movie_runtime = self.current_movie.get("runtime")
        if not movie_runtime or movie_runtime <= 0:
            xbmc.log("Movary: Play stopped but could not determine movie runtime, skipping webhook.", level=xbmc.LOGWARNING)
            return

        current_runtime_position = self.current_runtime_position
        if not current_runtime_position or current_runtime_position <= 0:
            xbmc.log("Movary: Play stopped but could not determine current runtime position, skipping webhook.", level=xbmc.LOGWARNING)
            return

        watched_percentage = (current_runtime_position / movie_runtime) * 100

        xbmc.log(f"Movary: Play stopped at {watched_percentage:.2f}% of movie", level=xbmc.LOGDEBUG)

        if watched_percentage >= 90:
            self.sendWebhookRequest()
        else:
            xbmc.log("Movary: Play stopped at less than 90%, not sending webhook.", level=xbmc.LOGINFO)

        self.current_movie = None

    def onPlayBackEnded(self):
        if not self.is_enabled or not self.current_movie:
            return
        xbmc.log(f"Movary: Play ended", level=xbmc.LOGINFO)
        self.stopWatchTimer()
        self.sendWebhookRequest()
        self.current_movie = None

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
            "tmdb_id": tmdb_id or None,
            "runtime": self.getTotalTime(),
        }

        xbmc.log(f"Movary: Detected playing movie: {self.current_movie}", level=xbmc.LOGINFO)

    def sendWebhookRequest(self):
        if not self.is_enabled:
            xbmc.log(f"Movary: Did not send played movie webhook. Addon not enabled.", level=xbmc.LOGDEBUG)
            return

        if not self.current_movie.get("tmdb_id"):
            xbmc.log(f"Movary: Did not send played movie webhook. Movie has no tmdb id: {self.current_movie}", level=xbmc.LOGINFO)
            self.show_message("Info: Play not logged")

            return

        payload = {
            "title": self.current_movie.get("title"),
            "uniqueIds": {
                "tmdbId" : self.current_movie.get("tmdb_id")
            },
        }
        headers = {'Content-Type': 'application/json'}

        if not self.webhook_url:
            xbmc.log(f"Movary: Did not send played movie webhook. Webhook URL not set.", level=xbmc.LOGERROR)
            self.show_message("Error: Play not logged")

            return

        try:
            xbmc.log(f"Movary: Sending played movie webhook request to [{self.webhook_url}] with payload: {payload}", level=xbmc.LOGDEBUG)

            request = urllib.request.Request(
                url=self.webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers
            )
            with urllib.request.urlopen(request) as response:
                xbmc.log(f"Movary: Played movie webhook request sent. Response code: {response.status}", level=xbmc.LOGDEBUG)

                self.show_message("Play was logged")
        except Exception as e:
            xbmc.log(f"Movary: Played movie webhook request failed to sent: {e}", level=xbmc.LOGERROR)
            self.show_message("Error: Play not logged")