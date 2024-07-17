import threading
import time
import curses

class CursorPulser:
    def __init__(self, window, pulse_interval=0.5):
        self.window = window
        self.pulse_interval = pulse_interval
        self.is_pulsing = False
        self.pulse_thread = None
        self.stop_event = threading.Event()

    def start_pulsing(self):
        if not self.is_pulsing:
            self.is_pulsing = True
            self.stop_event.clear()
            self.pulse_thread = threading.Thread(target=self._pulse_cursor)
            self.pulse_thread.daemon = True
            self.pulse_thread.start()

    def stop_pulsing(self):
        if self.is_pulsing:
            self.is_pulsing = False
            self.stop_event.set()
        curses.curs_set(0)  # Ensure cursor is hidden immediately

    def _pulse_cursor(self):
        while self.is_pulsing and not self.stop_event.is_set():
            curses.curs_set(1)  # Show cursor
            if self.stop_event.wait(self.pulse_interval):
                break
            curses.curs_set(0)  # Hide cursor
            if self.stop_event.wait(self.pulse_interval):
                break
        curses.curs_set(0)  # Ensure cursor is hidden when exiting
