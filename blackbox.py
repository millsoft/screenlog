import threading
import time
import activewindow


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

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution
        self.active_window = ''

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            #print('Doing something imporant in the background')
            current_window = activewindow.get_active_window3()
            if(current_window != self.active_window):
                self.active_window = current_window
                print(current_window['title'])

            time.sleep(self.interval)



example = Blackbox()
print('Checkpoint')


while True:
    time.sleep(2)

