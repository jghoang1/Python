import os

os.environ["DISPLAY"] = ":0"

import logging
import platform

import pyautogui
from autoclicker import AutoClicker
from common import move_and_click, get_input_shim
import time

logging.basicConfig(level=logging.DEBUG)

pyautogui.PAUSE = 0.005


class RobloxDeepSeaAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.input_shim = get_input_shim()
        self.root.title("Julius's Roblox Deep Sea Idle")
        self.collect_money_timer = self.add_timer(
            60, self.collect_money, "Collect Money", initial_time=5
        )
        self.gift_timer = self.add_timer(
            5 * 60, self.claim_gifts, "Claim Gifts", initial_time=15
        )
        self.reset_gifts = self.add_timer(
            100 * 60, self.reset_gifts, "Reset Gifts", initial_time=45
        )

        self.GIFT_X_COORDS = (810, 1130, 1450)
        self.GIFT_Y_COORDS = (530, 790, 1050)

    def reset_gifts(self):
        move_and_click(1960, 1240, max_dx=50, max_dy=20)

    def collect_money(self):
        self.input_shim.keyDown("s")
        time.sleep(0.5)
        self.input_shim.keyUp("s")
        self.input_shim.keyDown("w")
        time.sleep(1)
        self.input_shim.keyUp("w")

    def claim_gifts(self):
        if platform.system() == "Windows":
            # gifts
            for y in self.GIFT_Y_COORDS:
                for x in self.GIFT_X_COORDS:
                    move_and_click(x, y, max_dx=100, max_dy=100)
        elif platform.system() == "Darwin":
            pass


if __name__ == "__main__":
    my_autoclicker = RobloxDeepSeaAuto()
    if platform.system() == "Windows":
        my_autoclicker.root.geometry("500x200+2700+-300")
    elif platform.system() == "Darwin":
        my_autoclicker.root.geometry("300x150+800+100")
    my_autoclicker.mainloop()
