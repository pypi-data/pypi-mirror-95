#!/usr/bin/env python
#
# Copyright 2012 Martin Owens <doctormo@gmail.com>
# Copyright 2015 Ian Denhardt <ian@zenhack.net>
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#
"""
Threaded windows allow your application to do tasks involving heavy
computaion or downloading which will interface with the gui at
intersections, but for which you need the interface to remain responsive.
"""

import threading
import logging
import time

# Import the threaded window class like others
from gtkme import asyncme, GtkApp, Window


class AppWindow(Window):
    """Just like any other window, except with threads."""
    # Use the existing app
    name = 'simpleapp'
    task_lock = threading.Lock()

    def sample_signal(self, widget=None):
        result = asyncme.holding(self.task_lock,
                               self.thread_contents,
                               blocking=False)
        if result is not None:
            print("Thread Started! (see, not locked)")

    def thread_contents(self):
        while True:
            timer = 0
            # This is where the action happens.
            while timer < 100:
                time.sleep(1)
                print("Ping")
                timer += 1
                self.safe_set_button_label('Foo %d' % timer)
                # TODO: We need some way of detecting if the gtk mainloop has
                # exited, and stop. The old ThreadedWindow code set a variable
                # on shutdown called  self._closed that we could check. I (Ian)
                # can think of a couple ways to do this, but I don't full
                # understand what gtkme is doing with the mainloop invocation
                # yet. For now, the application continues to run after the main
                # window has been closed (since this thread is still running).

    @asyncme.mainloop_only
    def safe_set_button_label(self, foo):
        # It isn't safe to use Gtk widgets outside of the thread executing
        # Gtk's mainloop, so this function is decorated with mainloop_only.
        # This forces it to be run inside of the Gtk mainloop.
        self.widget("button1").set_label(foo)


class ThreadedWindowApp(GtkApp):
    """This Application loads threaded windows just like any other."""
    glade_dir = './'
    app_name = 'threadedwindowapp'
    windows = [ AppWindow ]


if __name__ == '__main__':
    try:
        app = ThreadedWindowApp(start_loop=True)
    except KeyboardInterrupt:
        logging.info("User Interputed")
    logging.debug("Exiting Application")





