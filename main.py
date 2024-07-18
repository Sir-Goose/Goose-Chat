import os
import sys
import pickle
from groq import Groq
import requests
import saved_chats_window
import saved_chats_window
import state
import curses
import chat_window
import conversation
import get_key
import logging
import threading

logging.basicConfig(filename='chat_app_debug.log', level=logging.DEBUG)

title = r"""
   ______                         ________          __
  / ____/___  ____  ________     / ____/ /_  ____ _/ /_
 / / __/ __ \/ __ \/ ___/ _ \   / /   / __ \/ __ `/ __/
/ /_/ / /_/ / /_/ (__  )  __/  / /___/ / / / /_/ / /_
\____/\____/\____/____/\___/   \____/_/ /_/\__,_/\__/
"""
active_models = []


# global state
# s = state.State()
def main(stdscr):
    #curses.curs_set(0)  # Hide the cursor
    #stdscr.clear()
    #stdscr.refresh()
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
        "Edit Config",
        "Quit"
    ]

    menu_buttons = [
        "n",
        "v",
        "m",
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
                sys.exit(0)
                break
            if key == ord('n'):
                # conversation_list = conversation.Conversation_List()
                conversation_list.add_chat()
                chat_window.Chat_window(
                    stdscr,
                    conversation_list,
                    len(conversation_list.chat_list) -1,
                    models=active_models,
                    name=conversation_list.chat_list[len(conversation_list.chat_list) -1].name,
                )
                break
            if key == ord('c'):
                break
            if key == ord('v'):
                saved_chats_window.Saved_chats_window(stdscr, conversation_list, models=active_models)
                display_home(stdscr)


def get_active_model_names():
    api_key = get_key.get_api_key()
    url = "https://api.groq.com/openai/v1/models"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        active_model_names = [model['id'] for model in data.get('data', []) if model.get('active', False)]
        global active_models
        active_models = active_model_names

    except requests.exceptions.RequestException as e:
        raise e
        active_models = []

if __name__ == "__main__":
    conversation_list = conversation.Conversation_List()
    thread = threading.Thread(target=get_active_model_names())
    thread.start()
    curses.wrapper(main)
