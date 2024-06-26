import conversation_box
import curses


class Chat_window:
    def __init__(self, stdscr, conversation=[]):
        self.stdscr = stdscr
        self.height, self.width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        self.draw_title()
        self.conversation_box = self.draw_conversation()
        self.draw_conversation()
        self.draw_input_box()
        self.draw_hotkeys()
        self.stdscr.refresh()
        self.main_loop()


    def draw_title(self):
        title = "Chat"
        start_x = max(0, (self.width // 2) - (len(title)// 2))
        self.stdscr.addstr(0, start_x, title)

    def draw_conversation(self):
        box_height, box_width = self.height - 10, self.width - 4
        start_y, start_x = 2, 2
        return conversation_box.ConversationBox(self.stdscr, box_height, box_width, start_y, start_x)


    def draw_input_box(self):
        pass

    def draw_hotkeys(self):
        pass

    def main_loop(self):
        while True:
            key = self.stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('a'):
                self.conversation_box.add_text("This is a new line of text.\n" * 5)
            elif key == curses.KEY_UP:
                self.conversation_box.scroll_up()
            elif key == curses.KEY_DOWN:
                self.conversation_box.scroll_down()

            self.stdscr.refresh()
