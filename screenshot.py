from mss import mss
import mss.tools
import app

from datetime import datetime
from pathlib import Path
from multiprocessing import Process, Queue
from subprocess import Popen, PIPE
import re

class Screenshot:
	screenshotPath = 'screenshots'

	def __init__(self):
		Path(self.screenshotPath).mkdir(parents=True, exist_ok=True)

	def getFilename(self):
		now = datetime.now()
		currentDayPath = self.screenshotPath + "/" + now.strftime("%Y/%m/%Y-%m-%d/")
		Path(currentDayPath).mkdir(parents=True, exist_ok=True)
		fullPath = currentDayPath + now.strftime("%Y-%m-%d--%H-%M-%S") + "-{mon}-{top}-{left}-{width}-{height}-{date}.jpg"
		return fullPath

	"create a screenshot of all desktops"
	def makeGlobalScreenshot(self):
		with mss.mss() as sct:
			filename = self.getFilename()
			print("Creating screenshot " + filename)
			sct.shot(mon=-1, output=filename)

	def makeCoordinatedScreenshot(self, le: app.LogEntry):
		filename = self.getFilename()
		print("making screenshot: " + filename)
		sct = mss.mss()
		print(sct.monitors)
		sct.shot(mon=0, output=filename)

#     def save(self, mon=0, output="monitor-{mon}.png", callback=None):






