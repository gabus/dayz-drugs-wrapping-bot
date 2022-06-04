import pyautogui
import time
import pydirectinput
from loguru import logger


class Bot:

    def __init__(self):
        self.combine_square_coordinates_x = 1100
        self.combine_square_coordinates_y = 1134

        self.top_left_square_x = 1754
        self.top_left_square_y = 446

        self.backpack_square_width = 68
        self.backpack_square_height = 68

        self.backpack_rows = 12  # =
        self.backpack_columns = 10  # ||

        self.current_square_row = 0
        self.current_square_column = 1

    def proclaimer(self):
        logger.warning("""
            Out of the box works with: 
                * 2456 x 1440 resolution. 
                * 120 capacity backpack. 
                * open inventory before starting the script
        """)

    def get_square_coordinates(self, column, row) -> tuple:
        x = self.top_left_square_x + self.backpack_square_width * column - self.backpack_square_width
        y = self.top_left_square_y + self.backpack_square_height * row - self.backpack_square_height
        return x, y

    def get_next_square(self) -> tuple:
        self.current_square_row = self.current_square_row + 1

        if self.current_square_row > self.backpack_rows:
            self.current_square_column = self.current_square_column + 1
            self.current_square_row = 1

        return self.current_square_column, self.current_square_row  # x, y

    def should_stop(self) -> bool:
        if self.current_square_row == self.backpack_rows and self.current_square_column == self.backpack_columns:
            return True
        return False

    def activate_game_window(self):
        pyautogui.moveTo(self.combine_square_coordinates_x, self.combine_square_coordinates_y, duration=0.2)
        pyautogui.mouseDown()
        time.sleep(0.2)
        pyautogui.mouseUp()
        time.sleep(0.5)

    def drag_item(self):
        column, row = self.get_next_square()
        x, y = self.get_square_coordinates(column, row)

        pyautogui.moveTo(x, y, duration=0.2)
        pyautogui.mouseDown()
        pyautogui.moveTo(self.combine_square_coordinates_x, self.combine_square_coordinates_y, duration=0.2)
        pyautogui.mouseUp()

    @staticmethod
    def combine_two_bags():
        time.sleep(0.2)
        pyautogui.mouseDown()
        time.sleep(4)
        pyautogui.mouseUp()

    def start(self):
        logger.info("starting loop")
        start_time = time.time()
        i = 0

        self.proclaimer()
        self.activate_game_window()

        while not self.should_stop():
            i = i + 1

            time.sleep(0.2)
            self.drag_item()
            time.sleep(0.2)
            self.drag_item()

            self.combine_two_bags()

            pydirectinput.press('tab')

            if i % 10 == 0:
                logger.info("Combined {} bags in {}min".format(i / 2, round((time.time() - start_time)/60, 2)))


if __name__ == '__main__':
    b = Bot()
    b.start()

