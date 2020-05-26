from mss import mss
import mss.tools
import time

from datetime import datetime
from pathlib import Path
from multiprocessing import Process, Queue
from subprocess import Popen, PIPE
import re

class ScreenLog:
	screenshotPath = 'screenshots'

	def __init__(self):
		Path(self.screenshotPath).mkdir(parents=True, exist_ok=True)

	def getFilename(self):
		now = datetime.now()
		currentDayPath = self.screenshotPath + "/" + now.strftime("%Y/%m/%Y-%m-%d/")
		Path(currentDayPath).mkdir(parents=True, exist_ok=True)
		fullPath = currentDayPath + now.strftime("%Y-%m-%d--%H-%M-%S") + ".jpg"
		return fullPath

	def makeScreenshot(self):
		with mss.mss() as sct:
			filename = self.getFilename()
			print("Creating screenshot " + filename)
			sct.shot(mon=-1, output=filename)


	def get_active_window(self):
		"""
		Get the currently active window.

		Returns
		-------
		string :
			Name of the currently active window.
		"""
		import sys
		active_window_name = None
		if sys.platform in ['linux', 'linux2']:
			root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)

			for line in root.stdout:
				m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', line)
				if m != None:
					id_ = m.group(1)
					id_w = Popen(['xprop', '-id', id_, 'WM_NAME'], stdout=PIPE)
					break

			if id_w != None:
				for line in id_w.stdout:
					match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", line)
					if match != None:
						return match.group("name")
		elif sys.platform in ['Windows', 'win32', 'cygwin']:
			# http://stackoverflow.com/a/608814/562769
			import win32gui
			window = win32gui.GetForegroundWindow()
			active_window_name = win32gui.GetWindowText(window)
		elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
			# http://stackoverflow.com/a/373310/562769
			from AppKit import NSWorkspace
			active_window_name = (NSWorkspace.sharedWorkspace()
								  .activeApplication()['NSApplicationName'])
		else:
			print("sys.platform={platform} is unknown. Please report."
				  .format(platform=sys.platform))
			print(sys.version)
		return active_window_name

	def start(self):
		while True:
			self.makeScreenshot()
			time.sleep(5)


SR = ScreenLog()
# print(SR.get_active_window_title());
#print(SR.get_active_window());
SR.start()