import os
import curses

class State:
    def __init__(self):
        self.stdscr = curses.initscr()
