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
        self.root.title("Julius's Roblox Simple Idle")
        self.shimmy_timer = self.add_timer(5, self.shimmy, "Shimmy")
        self.shimmy_left = True


    def shimmy(self):
        dir = "a" if self.shimmy_left else "d"
        pydirectinput.keyDown(dir)
        time.sleep(0.3)
        pydirectinput.keyUp(dir)
        self.shimmy_left = not self.shimmy_left

    def on_pause(self):
        pydirectinput.keyUp("w")
        pydirectinput.keyUp("a")
        pydirectinput.keyUp("s")
        pydirectinput.keyUp("d")






if __name__ == "__main__":
    my_autoclicker = RobloxSimpleAuto()
    my_autoclicker.mainloop()