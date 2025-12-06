import logging
import pydirectinput
from autoclicker import AutoClicker
import time
import sys
import os


logging.basicConfig(level=logging.INFO)


class MinecraftJavaAutoFisher(AutoClicker):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.fishing_audio_trigger = self.add_audio_trigger(self.filename, self.on_fish_bite, "Fishing Audio Trigger")
        self.eat_timer = self.add_timer(30 * 60, self.eat_food, "Eat Food", initial_playstate=False)
        self.sleep_timer = self.add_timer(5 * 60, self.sleep_in_bed, "Sleep in Bed", initial_playstate=False)

    def eat_food(self):
        pydirectinput.scroll(-1)
        self.delay()
        pydirectinput.mouseDown(button="right")
        time.sleep(5)
        pydirectinput.mouseUp(button="right")
        self.delay()
        pydirectinput.scroll(1)

    def sleep_in_bed(self):
        pydirectinput.keyDown("s")
        time.sleep(2)
        pydirectinput.keyUp("s")
        self.delay()
        pydirectinput.rightClick()
        time.sleep(10)
        pydirectinput.keyDown("w")
        time.sleep(2)
        pydirectinput.keyUp("w")

    def on_fish_bite(self):
        pydirectinput.rightClick()
        self.root.after(1000, pydirectinput.rightClick)

    def on_pause(self):
        pass


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        filename = os.path.join(sys._MEIPASS, "audio_files\\minecraft_fishing_catch_sound_short.wav")
    else:
        filename = "C:\\Users\\Julius\\Repos\\Python\\Projects\\autoclickerv2\\minecraft_java_audio_fisher\\audio_files\\minecraft_fishing_catch_sound_short.wav"

    my_autoclicker = MinecraftJavaAutoFisher(filename)
    my_autoclicker.mainloop()