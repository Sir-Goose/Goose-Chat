import curses
from curses import wrapper

class ConversationBox:
    def __init__(self, window, height, width, y, x):
        self.window = window
        self.height = height
        self.width = width
        self.y = y
        self.x = x
        self.box = window.subwin(height, width, y, x)
        self.box.box()
        self.text_win = self.box.derwin(height-2, width-2, 1, 1)
        self.text_win.scrollok(True)
        self.text_win.idlok(True)
        self.text = []
        self.scroll_pos = 0

    def add_text(self, new_text, new_line=True):
            if new_line:
                self.text.append(new_text)
            else:
                self.text[-1] += new_text
            self.scroll_to_bottom()
            self.refresh()

    def scroll_up(self):
        if self.scroll_pos > 0:
            self.scroll_pos -= 1
            self.refresh()

    def scroll_down(self):
        if self.scroll_pos < max(0, len(self.text) - (self.height - 2)):
            self.scroll_pos += 1
            self.refresh()

    def scroll_to_bottom(self):
        self.scroll_pos = max(0, len(self.text) - (self.height - 2))

    def refresh(self):
        self.text_win.clear()
        for i, line in enumerate(self.text[self.scroll_pos:self.scroll_pos + self.height - 2]):
            self.text_win.addstr(i, 0, line[:self.width-2])
        self.text_win.refresh()
