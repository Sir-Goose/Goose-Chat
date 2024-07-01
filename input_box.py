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
        # curses.curs_set(1) # make cursor visible
        pulser = cursor_pulsor.CursorPulser(self.window)
        pulser.start_pulsing()

        while True:
            self.input_area.clear()
            for i, line in enumerate(self.lines[self.scroll_pos:self.scroll_pos + self.height - 2]):
                self.input_area.addstr(i, 0, line[:self.width - 2])
            self.input_area.move(self.cursor_y - self.scroll_pos, self.cursor_x)
            self.win.refresh()
            self.input_area.refresh()

            key = self.input_area.getch()

            if key == 10:  # Enter key
                if self.cursor_y == len(self.lines) - 1:
                    self.lines.append("")
                else:
                    self.lines.insert(self.cursor_y + 1, self.lines[self.cursor_y][self.cursor_x:])
                    self.lines[self.cursor_y] = self.lines[self.cursor_y][:self.cursor_x]
                self.cursor_y += 1
                self.cursor_x = 0
                self.scroll_if_needed()
            elif key == ord('~'):  # send
                pulser.stop_pulsing()
                return "\n".join(self.lines).strip()
            elif key == 27: # escape
                pulser.stop_pulsing()
                return # empty return back to view mode
            elif key in (curses.KEY_BACKSPACE, 127):  # Backspace
                if self.cursor_x > 0:
                    self.lines[self.cursor_y] = self.lines[self.cursor_y][:self.cursor_x-1] + self.lines[self.cursor_y][self.cursor_x:]
                    self.cursor_x -= 1
                elif self.cursor_y > 0:
                    self.cursor_x = len(self.lines[self.cursor_y - 1])
                    self.lines[self.cursor_y - 1] += self.lines[self.cursor_y]
                    self.lines.pop(self.cursor_y)
                    self.cursor_y -= 1
                    self.scroll_if_needed()
            elif key == curses.KEY_LEFT:
                if self.cursor_x > 0:
                    self.cursor_x -= 1
                elif self.cursor_y > 0:
                    self.cursor_y -= 1
                    self.cursor_x = len(self.lines[self.cursor_y])
                    self.scroll_if_needed()
            elif key == curses.KEY_RIGHT:
                if self.cursor_x < len(self.lines[self.cursor_y]):
                    self.cursor_x += 1
                elif self.cursor_y < len(self.lines) - 1:
                    self.cursor_y += 1
                    self.cursor_x = 0
                    self.scroll_if_needed()
            elif key == curses.KEY_UP:
                if self.cursor_y > 0:
                    self.cursor_y -= 1
                    self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
                    self.scroll_if_needed()
            elif key == curses.KEY_DOWN:
                if self.cursor_y < len(self.lines) - 1:
                    self.cursor_y += 1
                    self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
                    self.scroll_if_needed()
            elif 32 <= key <= 126:  # Printable characters
                self.lines[self.cursor_y] = (self.lines[self.cursor_y][:self.cursor_x] +
                                             chr(key) +
                                             self.lines[self.cursor_y][self.cursor_x:])
                self.cursor_x += 1
        # hide the cursor again
        pulser.stop_pulsing()

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
