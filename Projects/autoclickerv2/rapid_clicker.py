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

pyautogui.PAUSE = 0.001

class RobloxSimpleAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Rapid Click")
        self.shimmy_timer = self.add_timer(0.001, pyautogui.click, "Click")
  

    def on_play(self):
        pyautogui.click()
        pyautogui.sleep(0.2)
        pydirectinput.keyDown("w")

    def on_pause(self):
        pydirectinput.keyUp("w")
        pydirectinput.mouseUp(button="left")

if __name__ == "__main__":
    my_autoclicker = RobloxSimpleAuto()
    my_autoclicker.mainloop()