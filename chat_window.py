class Chat_window:
    def __init__(self, stdscr, conversation=[]):
        self.stdscr = stdscr
        self.stdscr.clear()
        self.draw_title()
        self.draw_conversation()
        self.draw_input_box()
        self.draw_hotkeys()
        self.stdscr.refresh()

    def draw_title(self):
        pass

    def draw_conversation(self):
        pass

    def draw_input_box(self):
        pass

    def draw_hotkeys(self):
        pass
