import os

os.environ['DISPLAY'] = ':0'

import sys
# sys.path.append('C:\\Users\\Julius\\Repos\\Python\\Projects\\autoclickerv2')

import logging
import pyautogui
import pydirectinput
from autoclicker import AutoClicker
import time
from common import move_and_click

logging.basicConfig(level=logging.DEBUG)

pyautogui.PAUSE = 0.005

class RobloxTankGameAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Roblox Tank Game Idle")
        self.gift_timer = self.add_timer(60, self.claim_gifts, "Buy Food", initial_time=5)

    def claim_gifts(self):
        move_and_click(self, x=1800, y=1100, max_dx=150, max_dy=10)
        move_and_click(self, 1800, 750, max_dx=150, max_dy=10)
        move_and_click(self, 1800, 400, max_dx=150, max_dy=10)

if __name__ == "__main__":
    my_autoclicker = RobloxTankGameAuto()
    my_autoclicker.root.geometry("500x200+2700+-300")
    my_autoclicker.mainloop()