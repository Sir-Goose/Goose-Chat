import os
import pickle
from groq import Groq
import saved_chats_window
import saved_chats_window
import state
import curses
import chat_window
import conversation

title = r"""
   ______                         ________          __
  / ____/___  ____  ________     / ____/ /_  ____ _/ /_
 / / __/ __ \/ __ \/ ___/ _ \   / /   / __ \/ __ `/ __/
/ /_/ / /_/ / /_/ (__  )  __/  / /___/ / / / /_/ / /_
\____/\____/\____/____/\___/   \____/_/ /_/\__,_/\__/
"""


# global state
# s = state.State()
def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    stdscr.refresh()
    display_home(stdscr)


def display_home(stdscr):
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()  # Start color functionality
    # curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Initialize color pair 1
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Initialize color pair 1

    stdscr.clear()
    stdscr.refresh()

    # Get window dimensions
    height, width = stdscr.getmaxyx()

    # Split the title into lines
    title_lines = [line.strip() for line in title.strip().split('\n')]
    title_height = len(title_lines)
    title_width = max(len(line) for line in title_lines)

    # add the space back correctly
    title_lines[0] = "   " + title_lines[0]
    title_lines[1] = "  " + title_lines[1]
    title_lines[2] = " " + title_lines[2]

    # Calculate the position to center the title
    start_y = 1
    start_x = max(0, (width // 2) - (title_width // 2))

    # Display the title in green
    for i, line in enumerate(title_lines):
        stdscr.addstr(start_y + i, start_x, line, curses.color_pair(1))

    # Menu options
    menu_items = [
        "New Chat",
        "View Chats",
        "Change Model",
        "Quit"
    ]

    menu_buttons = [
        "n",
        "v",
        "c",
        "q"
    ]

    # Calculate position to center the menu items below the title
    menu_y = start_y + title_height + 2  # 2 lines below the title
    for item in menu_items:
        stdscr.addstr(menu_y, start_x, item)
        stdscr.addstr(menu_y, (start_x + title_width - 3), menu_buttons.pop(0))
        menu_y += 1

    # stdscr.addstr(5, 0, "New Chat\t\t\t\t\tn")
    # stdscr.addstr(4, 0, "View Chats\t\t\t\t\tv")
    # stdscr.addstr(6, 0, "Quit\t\t\t\t\t\tq")
    stdscr.refresh()

    while True:
            key = stdscr.getch()
            if key == ord('q'):
                break
            if key == ord('n'):
                # conversation_list = conversation.Conversation_List()
                conversation_list.add_chat()
                chat_window.Chat_window(
                    stdscr,
                    conversation_list,
                    len(conversation_list.chat_list) -1,
                    name=conversation_list.chat_list[len(conversation_list.chat_list) -1].name,
                )
                break
            if key == ord('c'):
                break
            if key == ord('v'):
                saved_chats_window.Saved_chats_window(stdscr, conversation_list)


def new_chat():
    key = "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"
    client = Groq(
    api_key=key,
    )
    conversation_history = []
    while True:
        print("user: ")
        user_message = input()
        conversation_history.append({"role": "user", "content": user_message})
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model="llama3-8b-8192",
        )
        print(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    conversation_list = conversation.Conversation_List()
    curses.wrapper(main)
