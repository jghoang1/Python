import os

os.environ["DISPLAY"] = ":0"

import logging
import platform
import time
import pyautogui
from autoclicker import AutoClicker
from common import move_and_click, get_input_shim

logging.basicConfig(level=logging.DEBUG)

pyautogui.PAUSE = 0.005


class RobloxDiceAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Dice Roblox Idle")
        self.input_shim = get_input_shim()
        self.dice_timer = self.add_timer(
            2.5 * 60, self.buy_dice, "Buy Dice", initial_time=15
        )
        self.roll_timer = self.add_timer(
            1 , self.roll_dice, "Roll Dice", initial_time=5,
        )

        self.X = 1500

    def buy_dice(self):
        if platform.system() == "Windows":
            move_and_click(2200, 630)
            time.sleep(3)
            move_and_click(2200, 630)
            time.sleep(3)
            move_and_click(2200, 630)

            move_and_click(
                self.X,
                600
                # 800
                ) # basic

            pyautogui.scroll(-5300)
            # move_and_click(self.X, 600) # omni
            pyautogui.scroll(-430)
            # move_and_click(self.X, 600) # wormhole
            pyautogui.scroll(-430)
            move_and_click(self.X, 600) # toxic
            pyautogui.scroll(-430)
            move_and_click(self.X, 600) # frozen
            pyautogui.scroll(-430)
            move_and_click(self.X, 600) # radioactive
            pyautogui.scroll(-430)
            move_and_click(self.X, 600) # blizzard


            move_and_click(1920, 300)

            move_and_click(1280, 1080, duration_max=0.5)

        elif platform.system() == "Darwin":
            pass

    def roll_dice(self):
        self.input_shim.click(1280, 1080, clicks=10, interval = 0.1)

if __name__ == "__main__":
    my_autoclicker = RobloxDiceAuto()
    if platform.system() == "Windows":
        my_autoclicker.root.geometry("500x200+2700+-300")
    elif platform.system() == "Darwin":
        my_autoclicker.root.geometry("300x150+800+100")
    my_autoclicker.mainloop()
