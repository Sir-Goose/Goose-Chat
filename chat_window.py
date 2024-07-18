from groq import Groq
from groq.types.chat import chat_completion
import conversation_box
import conversation
import input_box
import curses
import chat_engine
import get_key
import model_switcher

import logging

# Set up logging
logging.basicConfig(filename='chat_app_debug.log', level=logging.DEBUG)

# need to display the existing chat history
class Chat_window:
    def __init__(self, stdscr, conversation_list, chat_position, models=["llama3-8b-8192"], name="New Chat"):
        self.stdscr = stdscr
        self.chat_position = chat_position
        self.conversation_list = conversation_list
        self.conversation_history = conversation_list.chat_list[self.chat_position].conversation_history
        self.available_models = models
        self.model = models[0]
        self.name = name
        self.height, self.width = self.stdscr.getmaxyx()
        self.mode = 0 # view mode
        self.buffer = ""
        self.stdscr.clear()
        self.draw_title()
        self.conversation_box = self.draw_conversation()
        self.input_box = self.draw_input_box()
        self.draw_hotkeys()
        self.load_conversation_history()
        self.stdscr.refresh()
        self.main_loop()

    def load_conversation_history(self):
        for message in self.conversation_history:
            if message['role'] == 'user':
                self.conversation_box.add_text(f"User: {message['content']}\n", new_line=True)
            elif message['role'] == 'assistant':
                self.conversation_box.add_text(f"AI: {message['content']}\n", new_line=True)
        self.conversation_box.scroll_to_bottom()

    def draw_title(self):
        self.stdscr.move(0, 0)
        self.stdscr.clrtoeol()
        title = f"{self.name} - {self.model}"
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
        if self.mode == 0:
            self.draw_hotkeys_view_mode()
        else:
            self.draw_hotkeys_input_mode()
        # self.stdscr.addstr(self.height - 1, 2, "Esc: View Mode | A or I: Input Mode | ~: Send | Ctrl+C: Quit")

    def draw_hotkeys_view_mode(self):
        self.stdscr.move(self.height -1, 0)
        self.stdscr.clrtoeol()
        self.stdscr.addstr(self.height - 1, 2, "A or I: Input Mode | j/k: Navigate | Enter: Send | m: Model | q: Quit | w: Save")

    def draw_hotkeys_input_mode(self):
        # First, clear the existing content on the row
        self.stdscr.move(self.height - 1, 0)  # Move to the start of the row
        self.stdscr.clrtoeol()  # Clear from cursor to end of line
        self.stdscr.addstr(self.height - 1, 2, "Esc: View Mode")

    def prompt_for_chat_name(self):
            self.stdscr.move(self.height - 1, 0)
            self.stdscr.clrtoeol()
            self.stdscr.addstr(self.height - 1, 2, "Enter chat name: ")
            curses.echo()
            chat_name = self.stdscr.getstr(self.height - 1, 19, 50).decode('utf-8')
            curses.noecho()
            return chat_name

    def save_chat(self, new_name=None):
            if new_name:
                self.name = new_name
                self.conversation_list.chat_list[self.chat_position].name = new_name
            self.conversation_list.chat_list[self.chat_position].conversation_history = self.conversation_history
            self.conversation_list.chat_list[self.chat_position].update_timestamp()
            conversation.store_chats(self.conversation_list.chat_list)
            self.draw_title()  # Redraw the title with the new name


    def request_completion(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        chat_completion = chat_engine.completion(
            get_key.get_api_key(),
            self.model,
            self.conversation_history)

        response = chat_completion.choices[0].message.content
        return response

    def stream_completion(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        client = Groq(api_key=get_key.get_api_key())
        stream = client.chat.completions.create(
            messages=self.conversation_history,
            model=self.model,
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
                if key == 10:
                    if self.buffer:
                        self.send_message(self.buffer, streaming)
                        self.buffer = ""
                if key == ord('j'):
                    self.conversation_box.scroll_down()
                elif key == ord('k'):
                    self.conversation_box.scroll_up()
                elif key == ord('m'):
                    curses.curs_set(0)
                    popup = model_switcher.ModelSwitcherPopup(self.stdscr, self.available_models)
                    popup.draw()
                    new_model = popup.handle_input()
                    if new_model:
                        self.model = new_model
                        self.draw_title()
                    self.stdscr.touchwin()
                    self.stdscr.refresh()
                elif key == ord('q'):
                    self.save_chat()
                    break
                elif key == ord('w'):
                    chat_name = self.prompt_for_chat_name()
                    if chat_name:
                        self.save_chat(new_name=chat_name)
                        self.draw_hotkeys_view_mode()
                elif key == ord('i') or key == ord('a'):
                    self.draw_hotkeys_input_mode()
                    self.stdscr.refresh()
                    user_input = self.input_box.edit()
                    self.draw_hotkeys_view_mode()
                    # curses.curs_set(0)
                    if user_input:
                        self.buffer = user_input
        except KeyboardInterrupt:
            self.save_chat()
            pass

    def send_message(self, buffer, streaming):
        self.conversation_box.add_text(f"User: {buffer}\n", new_line=True)
        self.input_box.clear()
        if streaming:
            self.conversation_box.add_text("AI: ", new_line=True)
            self.stream_completion(buffer)
        else:
            response = self.request_completion(buffer)
            self.conversation_box.add_text(f"AI: {response}\n", new_line=True)

            self.conversation_box.scroll_to_bottom()

        self.conversation_box.refresh()
                #self.stdscr.refresh()
