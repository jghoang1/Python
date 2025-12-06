import os

os.environ['DISPLAY'] = ':0'

import logging
import pyautogui
import pydirectinput
from autoclicker import AutoClicker
import time
from common import move_and_click
import platform

logging.basicConfig(level=logging.DEBUG)

pyautogui.PAUSE = 0.005



class RobloxTankGameAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Roblox Tank Game Idle")
        self.gift_timer = self.add_timer(5*60, self.claim_gifts, "Claim Gifts", initial_time=5)

    def claim_gifts(self):
        if platform.system() == "Windows":
            move_and_click(self, 1124, 508, max_dx=1, max_dy=1)

            move_and_click(self, 925 , 545, max_dx=50, max_dy=10)
            move_and_click(self, 1160, 545, max_dx=50, max_dy=10)
            move_and_click(self, 1365, 545, max_dx=50, max_dy=10)
            move_and_click(self, 1610, 545, max_dx=50, max_dy=10)

            move_and_click(self, 925 , 735, max_dx=50, max_dy=10)
            move_and_click(self, 1160, 735, max_dx=50, max_dy=10)
            move_and_click(self, 1365, 735, max_dx=50, max_dy=10)
            move_and_click(self, 1610, 735, max_dx=50, max_dy=10)

            move_and_click(self, 925 , 925, max_dx=50, max_dy=10)
            move_and_click(self, 1160, 925, max_dx=50, max_dy=10)
            move_and_click(self, 1365, 925, max_dx=50, max_dy=10)
            move_and_click(self, 1610, 925, max_dx=50, max_dy=10)


if __name__ == "__main__":
    my_autoclicker = RobloxTankGameAuto()
    my_autoclicker.root.geometry("500x200+2700+-300")
    my_autoclicker.mainloop()