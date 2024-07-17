import curses
import cursor_pulsor

class MultilineChatInputBox:
    def __init__(self, window, height, width, y, x):
        self.window = window
        self.height = height
        self.width = width
        self.y = y
        self.x = x
        self.win = window.subwin(height, width, y, x)
        self.win.box()
        self.input_area = self.win.derwin(height - 2, width - 2, 1, 1)
        self.input_area.keypad(True)
        self.input_area.scrollok(True)
        self.lines = [""]
        self.cursor_y = 0
        self.cursor_x = 0
        self.scroll_pos = 0

    def edit(self):
        curses.set_escdelay(1)
        pulser = cursor_pulsor.CursorPulser(self.window)
        pulser.start_pulsing()
        #buffer = ""

        while True:
            self.refresh_display()

            try:
                key = self.input_area.get_wch()
                #buffer += str(key)
            except:
                continue

            if isinstance(key, str):
                key = ord(key)

            if key == 10:  # Enter key
                self.handle_enter()
            #elif key == ord('~'):  # send
                #pulser.stop_pulsing()
                #return "\n".join(self.lines).strip()
            elif key == 27:  # escape
                pulser.stop_pulsing()
                return "\n".join(self.lines).strip()
                #return  # empty return back to view mode
            elif key in (curses.KEY_BACKSPACE, 127):  # Backspace
                self.handle_backspace()
            elif key == curses.KEY_LEFT:
                self.handle_left()
            elif key == curses.KEY_RIGHT:
                self.handle_right()
            elif key == curses.KEY_UP:
                self.handle_up()
            elif key == curses.KEY_DOWN:
                self.handle_down()
            elif key == 22:  # Ctrl+V (paste)
                self.handle_paste()
            elif 32 <= key <= 126 or key > 127:  # Printable characters including multi-byte
                self.insert_char(chr(key))

        #pulser.stop_pulsing()

    def refresh_display(self):
        self.input_area.clear()
        for i, line in enumerate(self.lines[self.scroll_pos:self.scroll_pos + self.height - 2]):
            self.input_area.addstr(i, 0, line[:self.width - 2])
        self.input_area.move(self.cursor_y - self.scroll_pos, min(self.cursor_x, self.width - 3))
        self.win.refresh()
        self.input_area.refresh()

    def handle_enter(self):
        self.lines.insert(self.cursor_y + 1, self.lines[self.cursor_y][self.cursor_x:])
        self.lines[self.cursor_y] = self.lines[self.cursor_y][:self.cursor_x]
        self.cursor_y += 1
        self.cursor_x = 0
        self.scroll_if_needed()

    def handle_backspace(self):
        if self.cursor_x > 0:
            self.lines[self.cursor_y] = self.lines[self.cursor_y][:self.cursor_x-1] + self.lines[self.cursor_y][self.cursor_x:]
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            self.cursor_x = len(self.lines[self.cursor_y - 1])
            self.lines[self.cursor_y - 1] += self.lines[self.cursor_y]
            self.lines.pop(self.cursor_y)
            self.cursor_y -= 1
            self.scroll_if_needed()

    def handle_left(self):
        if self.cursor_x > 0:
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = len(self.lines[self.cursor_y])
            self.scroll_if_needed()

    def handle_right(self):
        if self.cursor_x < len(self.lines[self.cursor_y]):
            self.cursor_x += 1
        elif self.cursor_y < len(self.lines) - 1:
            self.cursor_y += 1
            self.cursor_x = 0
            self.scroll_if_needed()

    def handle_up(self):
        if self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
            self.scroll_if_needed()

    def handle_down(self):
        if self.cursor_y < len(self.lines) - 1:
            self.cursor_y += 1
            self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
            self.scroll_if_needed()

    def insert_char(self, char):
        self.lines[self.cursor_y] = (self.lines[self.cursor_y][:self.cursor_x] +
                                     char +
                                     self.lines[self.cursor_y][self.cursor_x:])
        self.cursor_x += 1
        if self.cursor_x >= self.width - 2:
            self.handle_enter()

    def handle_paste(self):
        content = self.get_clipboard_content()
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if i > 0:
                self.handle_enter()
            self.insert_text(line)

    def insert_text(self, text):
        for char in text:
            if char == '\n':
                self.handle_enter()
            else:
                self.insert_char(char)

    def scroll_if_needed(self):
        if self.cursor_y < self.scroll_pos:
            self.scroll_pos = self.cursor_y
        elif self.cursor_y >= self.scroll_pos + self.height - 2:
            self.scroll_pos = self.cursor_y - (self.height - 3)

    def clear(self):
        self.lines = [""]
        self.cursor_y = 0
        self.cursor_x = 0
        self.scroll_pos = 0
        self.input_area.clear()
        self.win.box()
        self.win.refresh()
        self.input_area.refresh()

    def get_clipboard_content(self):
        import subprocess
        try:
            return subprocess.check_output(['pbpaste']).decode('utf-8')
        except:
            try:
                return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o']).decode('utf-8')
            except:
                return ""
