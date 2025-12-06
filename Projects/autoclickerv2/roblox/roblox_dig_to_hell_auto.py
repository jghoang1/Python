import logging
import pyautogui
import pydirectinput
from pynput.keyboard import Key
from autoclicker import AutoClicker
import time
import random

logging.basicConfig(level=logging.ERROR)

pyautogui.PAUSE = 0.005

class RobloxDigToHellAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Roblox Dig To Hell Farm")
        self.attack_timer = self.add_timer(0.01, pyautogui.leftClick, "Left Click")
        self.inventory_switch_timer = self.add_timer(5, self.switch_inventory, "Switch Inventory")
        self.rebirth_timer = self.add_timer(3 * 60, self.rebirth, "Rebirth")

        self.walk_seq = self.add_sequence([("w", 10), 
                                           ("a", 10),
                                           ("w", 10),
                                           ("d", 10),
                                           ("w", 10),
                                           ("a", 10),
                                           ("s", 10), 
                                           ("d", 10),], "Walk")
        self.inventory_index = 0
        self.inventory_loop = ["1", "2"]

    def switch_inventory(self):
        pydirectinput.press(self.inventory_loop[self.inventory_index])
        self.inventory_index = (self.inventory_index + 1) % len(self.inventory_loop)

    def move_and_click(self, x, y, pause_after = 0.5):
        duration = random.uniform(0.1, 0.9)
        dx = random.randrange(-10,10)
        dy = random.randrange(-10,10)
        tween = random.choice((pyautogui.easeInQuad,
                               pyautogui.easeOutQuad,
                               pyautogui.easeInOutQuad,
                               pyautogui.easeInElastic))
        pyautogui.moveTo(x + dx, y + dy, duration=duration, tween = tween)
        pydirectinput.click(x + dx, y + dy, clicks = 1)
        time.sleep(pause_after)

    def rebirth(self):
        self.move_and_click(253, 708)
        self.move_and_click(1300, 980)
        self.move_and_click(1670, 340)
        self.move_and_click(2400, 38)


    def on_pause(self):
        pydirectinput.keyUp("w")
        pydirectinput.keyUp("a")
        pydirectinput.keyUp("s")
        pydirectinput.keyUp("d")






if __name__ == "__main__":
    my_autoclicker = RobloxDigToHellAuto()
    my_autoclicker.mainloop()