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
        self.root.title("Julius's Hair Cut Roblox Idle")
        self.input_shim = get_input_shim()
        self.dice_timer = self.add_timer(
            30, self.cut_hair, "Cut Hair", initial_time=5
        )

    def cut_hair(self):
        self.input_shim.press("e")
        move_and_click(1735, 1145, pause_after=0)
        time.sleep(.550)
        self.input_shim.click()
        time.sleep(1.8)
        self.input_shim.click()
        # time.sleep()
        # self.input_shim.click()e

if __name__ == "__main__":
    my_autoclicker = RobloxDiceAuto()
    if platform.system() == "Windows":
        my_autoclicker.root.geometry("500x200+2700+-300")
    elif platform.system() == "Darwin":
        my_autoclicker.root.geometry("300x150+800+100")
    my_autoclicker.mainloop()
