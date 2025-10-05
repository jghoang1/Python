import logging
import pyautogui
import pydirectinput
from autoclicker import AutoClicker

logging.basicConfig(level=logging.ERROR)

pyautogui.PAUSE = 0.005

DEFAULT_T = 15

class RobloxAdoptMeAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.root.title("Julius's Adopt Me Auto-Care")

        self.walk_seq = self.add_sequence([(["s", "space"], 0.25), ("s", DEFAULT_T), ("e", 0.1),
                                           (["s", "space"], 0.25), ("s", DEFAULT_T), ("e", 0.1), ("2", 0.1),
                                           (["a", "space"], 0.25), ("a", 20), ("e", 0.1),
                                           (["a", "space"], 0.25), ("a", DEFAULT_T), ("e", 0.1),
                                           (["w", "space"], 0.25), ("w", DEFAULT_T), ("e", 0.1),
                                           (["w", "space"], 0.25), ("w", DEFAULT_T), ("e", 0.1),
                                           (["d", "space"], 0.25), ("d", DEFAULT_T), ("e", 0.1),
                                           (["d", "space"], 0.25), ("d", DEFAULT_T), ("e", 0.1),
                                           ], "Walk")

    def on_pause(self):
        pydirectinput.keyUp("w")
        pydirectinput.keyUp("a")
        pydirectinput.keyUp("s")
        pydirectinput.keyUp("d")
        pydirectinput.keyUp("e")
        pydirectinput.keyUp("2")



if __name__ == "__main__":
    my_autoclicker = RobloxAdoptMeAuto()
    my_autoclicker.root.geometry("500x200+2700+-300") 
    my_autoclicker.mainloop()