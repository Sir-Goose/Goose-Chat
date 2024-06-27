from groq.types.chat import chat_completion
import conversation_box
import input_box
import curses
import chat_engine

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
        conversation_history = []
        try:
            while True:
                user_input = self.input_box.edit()
                if user_input:
                    self.conversation_box.add_text(f"User: {user_input}")
                    self.input_box.clear()

                    conversation_history.append({"role": "user", "content": user_input})
                    chat_completion = chat_engine.completion(
                        "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",
                        "llama3-8b-8192",
                        conversation_history)

                    response = chat_completion.choices[0].message.content
                    self.conversation_box.add_text(f"AI: {response}")
                self.stdscr.refresh()
        except KeyboardInterrupt:
            pass  # Exit the chat window on Ctrl+C
