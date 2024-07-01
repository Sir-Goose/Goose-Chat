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
        self.lines = []
        self.scroll_pos = 0

    def add_text(self, new_text, new_line=True):
        new_lines = new_text.split('\n')
        for i, line in enumerate(new_lines):
            if i > 0 or new_line:
                self.lines.append('')
            wrapped_lines = self._wrap_text(line)
            if wrapped_lines:
                self.lines[-1] += wrapped_lines[0]
                self.lines.extend(wrapped_lines[1:])
        self.scroll_to_bottom()
        self.refresh()

    def _wrap_text(self, text):
        wrapped_lines = []
        while text:
            if len(text) <= self.width - 2:
                wrapped_lines.append(text)
                break
            split_point = text.rfind(' ', 0, self.width - 2)
            if split_point == -1:
                split_point = self.width - 2
            wrapped_lines.append(text[:split_point])
            text = text[split_point:].lstrip()
        return wrapped_lines

    def scroll_up(self):
        if self.scroll_pos > 0:
            self.scroll_pos -= 1
            self.refresh()

    def scroll_down(self):
        if self.scroll_pos < max(0, len(self.lines) - (self.height - 2)):
            self.scroll_pos += 1
            self.refresh()

    def scroll_to_bottom(self):
        self.scroll_pos = max(0, len(self.lines) - (self.height - 2))

    def refresh(self):
        self.text_win.clear()
        for i, line in enumerate(self.lines[self.scroll_pos:self.scroll_pos + self.height - 2]):
            self.text_win.addstr(i, 0, line[:self.width-2])
        self.box.box()
        self.text_win.refresh()
        self.box.refresh()
