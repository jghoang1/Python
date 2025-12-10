import os

os.environ["DISPLAY"] = ":0"

import logging
import platform

import pyautogui
from autoclicker import AutoClicker
from common import move_and_click

logging.basicConfig(level=logging.DEBUG)

pyautogui.PAUSE = 0.005


class RobloxTankGameAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Roblox Tank Game Idle")
        self.gift_timer = self.add_timer(
            5 * 60, self.claim_gifts, "Claim Gifts", initial_time=5
        )

    def claim_gifts(self):
        if platform.system() == "Windows":
            # gifts
            move_and_click(self, 2350, 580, max_dx=10, max_dy=10)
            move_and_click(self, 1124, 508, max_dx=1, max_dy=1)

            move_and_click(self, 925, 545, max_dx=50, max_dy=10)
            move_and_click(self, 1160, 545, max_dx=50, max_dy=10)
            move_and_click(self, 1365, 545, max_dx=50, max_dy=10)
            move_and_click(self, 1610, 545, max_dx=50, max_dy=10)

            move_and_click(self, 925, 735, max_dx=50, max_dy=10)
            move_and_click(self, 1160, 735, max_dx=50, max_dy=10)
            move_and_click(self, 1365, 735, max_dx=50, max_dy=10)
            move_and_click(self, 1610, 735, max_dx=50, max_dy=10)

            move_and_click(self, 925, 925, max_dx=50, max_dy=10)
            move_and_click(self, 1160, 925, max_dx=50, max_dy=10)
            move_and_click(self, 1365, 925, max_dx=50, max_dy=10)
            move_and_click(self, 1610, 925, max_dx=50, max_dy=10)

            # rank
            move_and_click(self, 2410, 690, max_dx=100, max_dy=10)
            move_and_click(self, 930, 930, max_dx=50, max_dy=50)
            move_and_click(self, 930, 930, max_dx=50, max_dy=50)
        elif platform.system() == "Darwin":
            # gifts
            move_and_click(self, 1030, 310, max_dx=5, max_dy=5)
            # move_and_click(self, 1124, 508, max_dx=1, max_dy=1)

            move_and_click(self, 400, 300, max_dx=5, max_dy=5)
            move_and_click(self, 510, 300, max_dx=5, max_dy=5)
            move_and_click(self, 610, 300, max_dx=5, max_dy=5)
            move_and_click(self, 720, 300, max_dx=5, max_dy=5)

            move_and_click(self, 400, 400, max_dx=5, max_dy=5)
            move_and_click(self, 510, 400, max_dx=5, max_dy=5)
            move_and_click(self, 610, 400, max_dx=5, max_dy=5)
            move_and_click(self, 720, 400, max_dx=5, max_dy=5)

            move_and_click(self, 400, 500, max_dx=5, max_dy=5)
            move_and_click(self, 510, 500, max_dx=5, max_dy=5)
            move_and_click(self, 610, 500, max_dx=5, max_dy=5)
            move_and_click(self, 720, 500, max_dx=5, max_dy=5)

            # rank
            move_and_click(self, 1060, 375, max_dx=1, max_dy=1)
            move_and_click(self, 400, 470, max_dx=1, max_dy=1)
            move_and_click(self, 400, 470, max_dx=1, max_dy=1)


if __name__ == "__main__":
    my_autoclicker = RobloxTankGameAuto()
    if platform.system() == "Windows":
        my_autoclicker.root.geometry("500x200+2700+-300")
    elif platform.system() == "Darwin":
        my_autoclicker.root.geometry("300x150+800+100")
    my_autoclicker.mainloop()
