#!/usr/bin/env python

"""Find the currently active window."""

import logging
import sys
import subprocess
import gi


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)

def get_active_window3():
    command = "xdotool getactivewindow getwindowname"
    title = subprocess.check_output(["/bin/bash", "-c", command]).decode("utf-8").strip()

    command = "xdotool getactivewindow getwindowpid"
    pid = subprocess.check_output(["/bin/bash", "-c", command]).decode("utf-8").strip()

    command = "more /proc/" + pid + "/cmdline"
    cmdline = subprocess.check_output(["/bin/bash", "-c", command]).decode("utf-8").strip()
    re = {'title': title, 'pid': pid, 'cmdline': cmdline}
    print(re)
    return re




def get_active_window2():
    #command = "xprop -root _NET_ACTIVE_WINDOW | sed 's/.* //'"
    command = "xdotool getactivewindow getwindowname"
    frontmost = subprocess.check_output(["/bin/bash", "-c", command]).decode("utf-8").strip()
    return frontmost



def get_active_window():
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
        # Alternatives: http://unix.stackexchange.com/q/38867/4784
        try:
            import wnck
        except ImportError:
            logging.info("wnck not installed")
            wnck = None
        if wnck is not None:
            screen = wnck.screen_get_default()
            screen.force_update()
            window = screen.get_active_window()
            if window is not None:
                pid = window.get_pid()
                with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
                    active_window_name = f.read()
        else:
            try:
                import gi
                gi.require_version("Gtk", "3.0")
                gi.require_version("Wnck", "3.0")
                from gi.repository import Gtk, Wnck
                gi = "Installed"
            except ImportError:
                logging.info("gi.repository not installed")
                gi = None
            if gi is not None:
                Gtk.init([])  # necessary if not using a Gtk.main() loop
                screen = Wnck.Screen.get_default()
                screen.force_update()  # recommended per Wnck documentation
                active_window = screen.get_active_window()
                pid = active_window.get_pid()
                with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
                    active_window_name = f.read()
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

#print("Active window: %s" % str(get_active_window()))