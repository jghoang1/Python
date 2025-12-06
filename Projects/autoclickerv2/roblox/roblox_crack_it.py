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
        self.root.title("Julius's Roblox Crack It")
        self.t_interact = self.add_timer(1, self.interact, "Interact")

    def interact(self):
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