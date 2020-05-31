import threading
import time
import activewindow
import app
import time
import logging

from screenshot import Screenshot


class Blackbox(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.active_window = {}
        self.last_screenshot = {}
        self.screenshot_saved_at = 0

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:

            try:
                current_window = activewindow.get_active_window3()

                s = Screenshot(current_window)
                s.takeScreenshot()

                "compare the last and the current screenshot"
                screenshot_changed = self.last_screenshot != s.image

                if current_window.title != self.active_window:
                    # New Window detected
                    print("NEW window detected")
                    s.save()
                    self.screenshot_saved_at = time.time()
                    self.active_window = current_window.title


                else:
                    seconds_since_last_screenshot = time.time() - self.screenshot_saved_at
                    if screenshot_changed and seconds_since_last_screenshot > 10:
                        print("Same window and a screenshot changed after a while")
                        s.save()
                        self.screenshot_saved_at = time.time()

                self.last_screenshot = s.image

            except Exception as err:
                print("{0}".format(err))
                print("Some error occured!")

            time.sleep(self.interval)

logging.disable(logging.CRITICAL)

Blackbox()

while True:
    time.sleep(2)
