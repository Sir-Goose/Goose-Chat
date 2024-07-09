import curses
import chat_window
import conversation

class Saved_chats_window:
    def __init__(self, stdscr, conversation_list):
        self.stdscr = stdscr
        self.conversation_list = conversation_list
        self.chat_list = conversation_list.chat_list
        self.height, self.width = self.stdscr.getmaxyx()
        self.current_position = 0
        self.top_of_page = 0
        self.max_chats_per_page = self.height - 4  # Leave room for header and footer
        self.stdscr.clear()
        self.draw_window()
        self.main_loop()

    def draw_window(self):
        self.stdscr.clear()
        self.draw_title()
        self.draw_chats()
        self.draw_footer()
        self.stdscr.refresh()

    def draw_title(self):
        title = "Saved Chats"
        start_x = max(0, (self.width // 2) - (len(title) // 2))
        self.stdscr.addstr(0, start_x, title, curses.A_BOLD)

    def draw_chats(self):
        for i in range(self.max_chats_per_page):
            chat_index = self.top_of_page + i
            if chat_index < len(self.chat_list):
                chat = self.chat_list[chat_index]
                chat_name = chat.name[:self.width - 4]  # Truncate if too long
                if chat_index == self.current_position:
                    self.stdscr.addstr(i + 2, 2, chat_name, curses.A_REVERSE)
                else:
                    self.stdscr.addstr(i + 2, 2, chat_name)

    def draw_footer(self):
        footer = "j/k: Navigate | Enter: Open Chat | r: Rename | d: Delete | q: Quit"
        self.stdscr.addstr(self.height - 1, 0, footer)

    def main_loop(self):
        while True:
            key = self.stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('j'):
                self.move_cursor_down()
            elif key == ord('k'):
                self.move_cursor_up()
            elif key == ord('r'):
                self.rename_chat()
            elif key == ord('d'):
                self.delete_chat()
            elif key == 10:  # Enter key
                self.open_selected_chat()
            self.draw_window()

    def move_cursor_down(self):
        if self.current_position < len(self.chat_list) - 1:
            self.current_position += 1
            if self.current_position >= self.top_of_page + self.max_chats_per_page:
                self.top_of_page += 1

    def move_cursor_up(self):
        if self.current_position > 0:
            self.current_position -= 1
            if self.current_position < self.top_of_page:
                self.top_of_page -= 1

    def open_selected_chat(self):
        if 0 <= self.current_position < len(self.chat_list):
            chat = self.chat_list[self.current_position]
            chat_window.Chat_window(
                self.stdscr,
                self.conversation_list,
                self.current_position,
                name=chat.name
            )
            self.draw_window()  # Redraw the saved chats window when returning from chat

    def rename_chat(self):
        if 0 <= self.current_position < len(self.chat_list):
            chat = self.chat_list[self.current_position]

            # Clear the footer and prompt for new name
            self.stdscr.move(self.height - 1, 0)
            self.stdscr.clrtoeol()
            self.stdscr.addstr(self.height - 1, 0, f"Enter new name for '{chat.name}': ")
            self.stdscr.refresh()

            # Get user input
            curses.echo()
            new_name = self.stdscr.getstr(self.height - 1, len(f"Enter new name for '{chat.name}': ")).decode('utf-8')
            curses.noecho()

            if new_name:
                # Update the chat name
                chat.name = new_name
                # Save the updated chat list
                # self.conversation_list.save_chats()
                conversation.store_chats(self.conversation_list.chat_list)

            self.draw_window()

    def delete_chat(self):
        if 0 <= self.current_position < len(self.chat_list):
            chat = self.chat_list[self.current_position]

            self.stdscr.move(self.height - 1, 0)
            self.stdscr.clrtoeol()
            self.stdscr.addstr(self.height - 1, 0, f"Delete chat '{chat.name}'? y/n: ")
            self.stdscr.refresh()

            curses.echo()
            confirmation = self.stdscr.getstr(self.height - 1, len(f"Delete chat '{chat.name}'? y/n: ")).decode('utf-8')
            curses.noecho()

            if confirmation == 'y':
                self.chat_list.pop(self.current_position)
                conversation.store_chats(self.conversation_list.chat_list)

            self.draw_window()
