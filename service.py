import xbmc

from resources.lib.movary_monitor import MovaryMonitor

def main():
    monitor = MainMonitor()

    xbmc.log("Movary: Starting addon", level=xbmc.LOGINFO)

    monitor.waitForAbort()

    xbmc.log("Movary: Stopping addon", level=xbmc.LOGINFO)

if __name__ == '__main__':
    main()