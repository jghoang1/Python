import logging
import pyautogui
import pydirectinput
from pynput.keyboard import Key
from autoclicker import AutoClicker
import time

logging.basicConfig(level=logging.DEBUG)

class RobloxUp(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Roblox")


    def on_pause(self):
        pydirectinput.keyUp("w")
        pydirectinput.keyDown("w")

        
    def on_play(self):
        pydirectinput.keyUp("w")

if __name__ == "__main__":
    my_autoclicker = RobloxUp()
    my_autoclicker.mainloop()