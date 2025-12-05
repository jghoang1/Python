import os

os.environ['DISPLAY'] = ':0'

import logging
import pyautogui
import pydirectinput
from autoclicker import AutoClicker
import time
from common import move_and_click

logging.basicConfig(level=logging.DEBUG)

pyautogui.PAUSE = 0.005

class RobloxSimpleAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Roblox Simple Idle")
        # self.shimmy_timer = self.add_timer(60, self.jump, "Jump", initial_time=5)
        self.food_timer = self.add_timer(60, self.buy_food, "Buy Food", initial_time=5)

    def jump(self):
        pydirectinput.keyDown("space")
        time.sleep(0.1)
        pydirectinput.keyUp("space")

    def on_pause(self):
        pydirectinput.keyUp("space")
        pydirectinput.keyUp("w")
        pydirectinput.keyUp("a")
        pydirectinput.keyUp("s")
        pydirectinput.keyUp("d")

    def buy_food(self):
        move_and_click(self, x=1800, y=1100, max_dx=150, max_dy=10)
        move_and_click(self, 1800, 750, max_dx=150, max_dy=10)
        move_and_click(self, 1800, 400, max_dx=150, max_dy=10)



if __name__ == "__main__":
    my_autoclicker = RobloxSimpleAuto()
    my_autoclicker.root.geometry("500x200+2700+-300")
    my_autoclicker.mainloop()