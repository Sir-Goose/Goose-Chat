import conversation_box
import input_box
import curses

class Chat_window:
    def __init__(self, stdscr, conversation=[]):
        self.stdscr = stdscr
        self.height, self.width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        self.draw_title()
        self.conversation_box = self.draw_conversation()
        self.input_box = self.draw_input_box()
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
        input_height = 5  # Increased height for multiple lines
        input_width = self.width - 4
        input_y = self.height - input_height - 1
        input_x = 2
        return input_box.MultilineChatInputBox(self.stdscr, input_height, input_width, input_y, input_x)

    def draw_hotkeys(self):
        self.stdscr.addstr(self.height - 1, 2, "Esc: Send | Ctrl+C: Quit")

    def main_loop(self):
        try:
            while True:
                user_input = self.input_box.edit()
                if user_input:
                    self.conversation_box.add_text(f"You: {user_input}")
                    self.input_box.clear()
                    # Here you would typically send the user_input to your chat model
                    # and then add the response to the conversation box
                    # For now, we'll just echo the input
                    self.conversation_box.add_text(f"Echo: {user_input}")
                self.stdscr.refresh()
        except KeyboardInterrupt:
            pass  # Exit the chat window on Ctrl+C
