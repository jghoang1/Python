import logging
import pydirectinput
from autoclicker import AutoClicker
import time

logging.basicConfig(level=logging.DEBUG)

class MinecraftAutoMiner(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Minecraft Auto-Skeleton Farm")
        self.attack_timer = self.add_timer(1, pydirectinput.leftClick, "Left Click")
        self.eat_timer = self.add_timer(5 * 60, self.eat_food, "Eat Food", initial_time=5, initial_playstate=False)
        self.sleep_timer = self.add_timer(5 * 60, self.sleep_in_bed, "Sleep in Bed", initial_playstate=False)
        self.shimmy_timer = self.add_timer(5, self.shimmy, "Shimmy")
        self.shimmy_left = True


    def shimmy(self):
        dir = "a" if self.shimmy_left else "d"
        pydirectinput.keyDown(dir)
        time.sleep(0.3)
        pydirectinput.keyUp(dir)
        self.shimmy_left = not self.shimmy_left


    def eat_food(self):
        pydirectinput.keyDown("s")
        time.sleep(2)
        pydirectinput.keyUp("s")
        self.delay()

        pydirectinput.press("2")

        self.delay()
        pydirectinput.mouseDown(button="right")
        time.sleep(5)
        pydirectinput.mouseUp(button="right")
        self.delay()

        pydirectinput.press("1")

        pydirectinput.keyDown("w")
        time.sleep(3)
        pydirectinput.keyDown("shift")
        time.sleep(3)
        pydirectinput.keyUp("w")
        pydirectinput.keyUp("shift")
    
    def sleep_in_bed(self):
        pydirectinput.keyDown("s")
        time.sleep(6)
        pydirectinput.keyUp("s")
        self.delay()

        pydirectinput.rightClick()

        time.sleep(10)
        pydirectinput.keyDown("w")
        time.sleep(4)
        pydirectinput.keyDown("shift")
        time.sleep(3)
        pydirectinput.keyUp("w")
        pydirectinput.keyDown("shift")
    


if __name__ == "__main__":
    my_autoclicker = MinecraftAutoMiner()
    my_autoclicker.mainloop()