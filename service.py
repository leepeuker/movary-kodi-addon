import time
import xbmc

if __name__ == '__main__':
    monitor = xbmc.Monitor()
    xbmc.log("Starting Movary addon", level=xbmc.LOGINFO)

    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break
