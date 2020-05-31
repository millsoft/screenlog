import pyautogui
from mss import mss
import mss.tools
import app

from datetime import datetime
from pathlib import Path
from multiprocessing import Process, Queue
from subprocess import Popen, PIPE
import re


class Screenshot:
    screenshotPath = 'data/screenshots'

    def __init__(self, log_entry: app.LogEntry):
        self.log_entry = log_entry
        self.image = None
        Path(self.screenshotPath).mkdir(parents=True, exist_ok=True)


    def getFilename(self):
        now = datetime.now()
        currentDayPath = self.screenshotPath + "/" + now.strftime("%Y/%m/%Y-%m-%d/")
        Path(currentDayPath).mkdir(parents=True, exist_ok=True)
        fullPath = currentDayPath + now.strftime("%Y-%m-%d--%H-%M-%S") + ".jpg"
        return fullPath

    def makeGlobalScreenshot(self):
        """create a screenshot of all desktops"""

        with mss.mss() as sct:
            filename = self.getFilename()
            print("Creating screenshot " + filename)
            sct.shot(mon=-1, output=filename)

    def save(self):
        """save the taken screenshot to disk"""

        filename = self.getFilename()
        self.image.save(filename)
        return filename

    def takeScreenshot(self):
        le = self.log_entry
        window = (le.window_location.x, le.window_location.y, le.window_size.width, le.window_size.height)
        self.image = pyautogui.screenshot(region=window)
