import logging
import pyautogui
from autoclicker import AutoClicker
import time

logging.basicConfig(level=logging.DEBUG)

class MinecraftAutoFisher(AutoClicker):
    def __init__(self):
        super().__init__()
        self.right_click_timer = self.add_timer(15, pyautogui.rightClick, "Right Click", initial_time=2)
        self.eat_timer = self.add_timer(30 * 60, self.eat_food, "Eat Food")
        self.sleep_timer = self.add_timer(5 * 60, self.sleep_in_bed, "Sleep in Bed")

    def eat_food(self):
        pyautogui.scroll(-1)
        self.delay()
        pyautogui.mouseDown(button="right")
        time.sleep(5)
        pyautogui.mouseUp(button="right")
        self.delay()
        pyautogui.scroll(1)

    def sleep_in_bed(self):
        pyautogui.keyDown("s")
        time.sleep(2)
        pyautogui.keyUp("s")
        self.delay()
        pyautogui.rightClick()
        time.sleep(10)
        pyautogui.keyDown("w")
        time.sleep(2)
        pyautogui.keyUp("w")

    def on_pause(self):
        self.right_click_timer.remaining_time = 2
    

if __name__ == "__main__":
    my_autoclicker = MinecraftAutoFisher()
    my_autoclicker.mainloop()