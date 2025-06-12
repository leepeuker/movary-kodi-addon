import xbmc

class MovaryPlayer(xbmc.Player):
    def __init__(self):
        super().__init__()

    def onAVStarted(self):
        xbmc.log(f"Movary: Play started", level=xbmc.LOGINFO)

    def onPlayBackPaused(self):
        xbmc.log(f"Movary: Play paused", level=xbmc.LOGINFO)

    def onPlayBackResumed(self):
        xbmc.log(f"Movary: Play resumed", level=xbmc.LOGINFO)

    def onPlayBackEnded(self):
        xbmc.log(f"Movary: Play ended", level=xbmc.LOGINFO)
