import logging
import pydirectinput
from autoclicker import AutoClicker
import time

logging.basicConfig(level=logging.DEBUG)

class MinecraftAutoMiner(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Minecraft Auto-Miner")
        self.eat_timer = self.add_timer(30 * 60, self.eat_food, "Eat Food")
        self.walk_timer = self.add_timer(10, self.stagger_walk, "Stagger Walk")

    def eat_food(self):
        pydirectinput.scroll(-1)
        self.delay()
        pydirectinput.mouseDown(button="right")
        time.sleep(5)
        pydirectinput.mouseUp(button="right")
        self.delay()
        pydirectinput.scroll(1)

    def reset_hold_left(self):
        pydirectinput.mouseUp(button="left")
        pydirectinput.mouseDown(button="left")

    def reset_sneak(self):
        pydirectinput.keyUp("shift")
        pydirectinput.keyDown("shift")

    def stagger_walk(self):
        pydirectinput.keyUp("w")
        time.sleep(0.5)
        pydirectinput.keyDown("w")

    def on_pause(self):
        pydirectinput.mouseUp(button="left")
        pydirectinput.keyUp("w")
        pydirectinput.keyDown("s")
        time.sleep(0.2)
        pydirectinput.keyUp("s")
        pydirectinput.keyUp("shift")

        
    def on_play(self):
        pydirectinput.keyDown("shift")
        pydirectinput.keyDown("w")
        pydirectinput.mouseDown(button="left")

if __name__ == "__main__":
    my_autoclicker = MinecraftAutoMiner()
    my_autoclicker.mainloop()