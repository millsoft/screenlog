import threading
import activewindow
import time
import logging
import data

from screenshot import Screenshot


class Blackbox(object):

    def __init__(self, interval=1):
        self.interval = interval
        self.active_window = {}
        self.last_screenshot = {}
        self.screenshot_saved_at = 0
        self.data = None

        print("Blackbox started")

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()


    def run(self):
        """ Method that runs forever """
        self.data = data.Data()
        print("Blackbox Thread!")

        while True:

            try:
                current_window = activewindow.get_active_window3()

                s = Screenshot(current_window)
                s.takeScreenshot()

                "compare the last and the current screenshot"
                screenshot_changed = self.last_screenshot != s.image
                save = False

                if current_window.title != self.active_window:
                    save = True
                    # New Window detected
                    print("NEW window detected")
                    self.active_window = current_window.title

                else:
                    seconds_since_last_screenshot = time.time() - self.screenshot_saved_at
                    if screenshot_changed and seconds_since_last_screenshot > 10:
                        save = True
                        print("Same window, but screenshot changed after a while")

                if save:
                    screenshot_filename = s.save()
                    self.screenshot_saved_at = time.time()
                    current_window.screenshot_filename = screenshot_filename
                    self.data.insert(current_window)

                self.last_screenshot = s.image

            except Exception as err:
                print("{0}".format(err))
                print("Some error occured!")

            time.sleep(self.interval)


# Disable Logs:
logging.disable(logging.CRITICAL)

Blackbox()

while True:
    time.sleep(2)
