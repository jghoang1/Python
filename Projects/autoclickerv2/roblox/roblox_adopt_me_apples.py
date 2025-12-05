import os

os.environ['DISPLAY'] = ':0'

import logging
import pyautogui
import pydirectinput
from pynput.keyboard import Key
from autoclicker import AutoClicker
import time
import random

logging.basicConfig(level=logging.DEBUG)

pyautogui.PAUSE = 0.005

class RobloxSimpleAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Roblox Adopt Me Box Clicker")
        self.box_timer = self.add_timer(60 * 10.2, self.open_box, "Open Box", initial_time=5)

    def open_box(self):
        pydirectinput.press("e")

    def on_pause(self):
        pydirectinput.keyUp("w")
        pydirectinput.keyUp("a")
        pydirectinput.keyUp("s")
        pydirectinput.keyUp("d")
        pydirectinput.keyUp("e")


if __name__ == "__main__":
    my_autoclicker = RobloxSimpleAuto()
    my_autoclicker.mainloop()