import curses
import logging

# Set up logging
logging.basicConfig(filename='chat_app_debug.log', level=logging.DEBUG)

class ModelSwitcherPopup:
    def __init__(self, stdscr, available_models):
        self.stdscr = stdscr
        self.available_models = available_models
        self.height, self.width = stdscr.getmaxyx()
        self.window = self.create_window()
        self.selected_index = 0
        logging.debug("ModelSwitcherPopup initialized")

    def create_window(self):
        max_model_length = max(len(model) for model in self.available_models)
        window_width = max(40, max_model_length + 6)  # Add padding for borders and selector
        height = min(len(self.available_models) + 4, self.height - 4)
        width = min(window_width, self.width - 4)
        start_y = (self.height - height) // 2
        start_x = (self.width - width) // 2
        window = curses.newwin(height, width, start_y, start_x)
        window.keypad(True)  # Enable keypad input
        logging.debug(f"Window created: height={height}, width={width}, start_y={start_y}, start_x={start_x}")
        return window

    def draw(self):
        self.window.erase()
        self.window.box()
        self.window.addstr(1, 2, "Select a model:")
        max_width = self.window.getmaxyx()[1] - 4  # Maximum width for model names
        for i, model in enumerate(self.available_models):
            y = i + 2
            if y >= self.window.getmaxyx()[0] - 1:  # Check if we're about to go out of bounds
                break
            if i == self.selected_index:
                self.window.addstr(y, 2, "> " + model[:max_width-2], curses.A_REVERSE)
            else:
                self.window.addstr(y, 2, "  " + model[:max_width-2])
        self.window.refresh()
        logging.debug(f"Draw completed. Selected index: {self.selected_index}")

    def handle_input(self):
        self.draw()
        while True:
            key = self.window.getch()
            logging.debug(f"Key pressed: {key}")
            if key == ord('q'):
                logging.debug("Quit key pressed")
                return None
            elif key == curses.KEY_UP or key == ord('k'):
                self.selected_index = max(0, self.selected_index - 1)
                logging.debug(f"Up key pressed. New index: {self.selected_index}")
            elif key == curses.KEY_DOWN or key == ord('j'):
                self.selected_index = min(len(self.available_models) - 1, self.selected_index + 1)
                logging.debug(f"Down key pressed. New index: {self.selected_index}")
            elif key in [10, 13]:  # Enter key
                logging.debug(f"Enter key pressed. Returning model: {self.available_models[self.selected_index]}")
                return self.available_models[self.selected_index]
            self.draw()  # Redraw after each key press
