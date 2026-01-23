import logging
from common import get_input_shim
from autoclicker import AutoClicker
import time

logging.basicConfig(level=logging.DEBUG)


class RobloxSimpleAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.input_shim = get_input_shim()
        self.input_shim.PAUSE = 0.005
        self.root.title("Julius's Roblox Simple Idle")
        self.input_shim = get_input_shim()
        self.shimmy_timer = self.add_timer(5, self.shimmy, "Shimmy", initial_playstate=False)
        self.shimmy_left = True
        self.click_timer = self.add_timer(1.0, self.click, "Click", initial_playstate=False)
        self.rapid_click_timer = self.add_timer(0, self.click, "Rapid Click", initial_playstate=False)

    def click(self):
        self.input_shim.click()

    def shimmy(self):
        dir = "a" if self.shimmy_left else "d"
        self.input_shim.keyDown(dir)
        time.sleep(0.3)
        self.input_shim.keyUp(dir)
        self.shimmy_left = not self.shimmy_left

    def on_pause(self):
        self.input_shim.keyUp("w")
        self.input_shim.keyUp("a")
        self.input_shim.keyUp("s")
        self.input_shim.keyUp("d")

    def click(self):
        self.input_shim.click()




if __name__ == "__main__":
    my_autoclicker = RobloxSimpleAuto()
    my_autoclicker.mainloop()