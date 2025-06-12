import xbmc

from resources.lib.movary_monitor import MovaryMonitor
from resources.lib.movary_player import MovaryPlayer

def main():
    monitor = MovaryMonitor()
    player = MovaryPlayer()

    xbmc.log("Movary: Starting addon", level=xbmc.LOGINFO)

    monitor.waitForAbort()

    xbmc.log("Movary: Stopping addon", level=xbmc.LOGINFO)

if __name__ == '__main__':
    main()