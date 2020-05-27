import threading
import time
import activewindow
import app

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
        self.test_a = {}

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution


    def run(self):
        """ Method that runs forever """
        while True:

            try:
                current_window = activewindow.get_active_window3()

                if current_window.title != self.active_window:
                    # New Window detected
                    self.active_window = current_window.title

                    s = Screenshot()
                    print(current_window.window_size)
                    s.makeCoordinatedScreenshot(current_window)

            except Exception as err:
                print("{0}".format(err))
                print("Some error occured!")


            time.sleep(self.interval)



example = Blackbox()
print('Checkpoint')


while True:
    time.sleep(2)

