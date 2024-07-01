from groq import Groq
from groq.types.chat import chat_completion
import conversation_box
import input_box
import curses
import chat_engine

class Chat_window:
    def __init__(self, stdscr, conversation):
        self.stdscr = stdscr
        self.conversation_history = conversation
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
        input_height = 6
        input_width = self.width - 4
        input_y = self.height - input_height - 1
        input_x = 2
        return input_box.MultilineChatInputBox(self.stdscr, input_height, input_width, input_y, input_x)

    def draw_hotkeys(self):
        self.stdscr.addstr(self.height - 1, 2, "Esc: View Mode | A or I: Input Mode | ~: Send | Ctrl+C: Quit")

    def request_completion(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        chat_completion = chat_engine.completion(
            "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",
            "llama3-8b-8192",
            self.conversation_history)

        response = chat_completion.choices[0].message.content
        return response

    def stream_completion(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        client = Groq(api_key="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")
        stream = client.chat.completions.create(
            messages=self.conversation_history,
            model="llama3-70b-8192",
            stream=True
        )

        full_response = ""
        buffer = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                buffer += delta
                if '\n' in buffer:
                    lines = buffer.split('\n')
                    for line in lines[:-1]:
                        self.conversation_box.add_text(line + '\n', new_line=False)
                    buffer = lines[-1]
                self.conversation_box.refresh()
                self.stdscr.refresh()
                full_response += delta

        if buffer:
            self.conversation_box.add_text(buffer + '\n', new_line=False)
        self.conversation_history.append({"role": "assistant", "content": full_response})

    def main_loop(self):
        streaming = True
        try:
            while True:
                key = self.stdscr.getch()
                if key == ord('j'):
                    self.conversation_box.scroll_down()
                elif key == ord('k'):
                    self.conversation_box.scroll_up()
                elif key == ord('i') or key == ord('a'):
                    user_input = self.input_box.edit()
                    # curses.curs_set(0)
                    if user_input:
                        self.conversation_box.add_text(f"User: {user_input}\n", new_line=True)
                        self.input_box.clear()
                        if streaming:
                            self.conversation_box.add_text("AI: ", new_line=False)
                            self.stream_completion(user_input)
                        else:
                            response = self.request_completion(user_input)
                            self.conversation_box.add_text(f"AI: {response}\n", new_line=True)

                        self.conversation_box.scroll_to_bottom()

                self.conversation_box.refresh()
                self.stdscr.refresh()
        except KeyboardInterrupt:
            pass
