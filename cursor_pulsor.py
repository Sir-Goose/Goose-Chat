import curses
import threading
import time

class CursorPulser:
    def __init__(self, window, pulse_interval=0.5):
        self.window = window
        self.pulse_interval = pulse_interval
        self.is_pulsing = False
        self.pulse_thread = None

    def start_pulsing(self):
        if not self.is_pulsing:
            self.is_pulsing = True
            self.pulse_thread = threading.Thread(target=self._pulse_cursor)
            self.pulse_thread.daemon = True
            self.pulse_thread.start()

    def stop_pulsing(self):
        self.is_pulsing = False
        if self.pulse_thread:
            self.pulse_thread.join()

    def _pulse_cursor(self):
        while self.is_pulsing:
            curses.curs_set(1)  # Show cursor
            time.sleep(self.pulse_interval)

            curses.curs_set(0)  # Hide cursor
            time.sleep(self.pulse_interval)
