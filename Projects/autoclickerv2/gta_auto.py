
import logging
import pydirectinput
from pynput.keyboard import Key
from autoclicker import AutoClicker
import time
import random
import tkinter as tk
import tkinter.ttk as ttk

logging.basicConfig(level=logging.INFO)

pydirectinput.PAUSE = 0.005

class GTAAuto(AutoClicker):
    def __init__(self):
        super().__init__()
        self.title.set("GTA Idle and Velum Flyer")
        self.root.title("Julius's GTA Simple Idle")
        
        self.shimmy_timer, _ = self.add_timer(5, self.shimmy, "Shimmy (j)", keybind="j")
        self.shimmy_left = True

        self.FLY_PLANE_WAVELENGTH = 1.5
        self.DUTY_CYCLE_STEP = 0.05
        self.duty_cycle = .1


        self.fly_plane_timer, self.fly_plane_row = self.add_timer(1, self.fly_plane, "Fly Plane (k,o,l, i)", initial_playstate=False, keybind="k")
        self.pressing_num5 = False

        # Add column to timer row for duty cycle
        # Col 4 : Duty Cycle
        self.duty_cycle_var = tk.StringVar()
        self.duty_cycle_var.set(str(self.duty_cycle))
        self.fly_plane_row.duty_label = ttk.Label(self.fly_plane_row.parent.frm, textvariable=self.duty_cycle_var)
        self.fly_plane_row.duty_label.grid(column=4, row=self.fly_plane_row.parent.current_row-1)

        # Add column to timer row for Direction
        # Col 5 : Direction
        self.direction_up = True
        self.direction_var = tk.StringVar()
        self.direction_var.set("Up")
        self.fly_plane_row.direction_label = ttk.Label(self.fly_plane_row.parent.frm, textvariable=self.direction_var)
        self.fly_plane_row.direction_label.grid(column=5, row=self.fly_plane_row.parent.current_row-1)


        self.swim_timer, _ = self.add_timer(3, self.swim, "Swim (u)", keybind="u", initial_playstate=False)

        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        self.keybinds["o"] = self.duty_cycle_up
        self.keybinds["l"] = self.duty_cycle_down
        self.keybinds["i"] = self.toggle_dir



    def shimmy(self):
        dir = "a" if self.shimmy_left else "d"
        pydirectinput.keyDown(dir)
        time.sleep(0.3)
        pydirectinput.keyUp(dir)
        self.shimmy_left = not self.shimmy_left

    def on_pause(self):
        pydirectinput.keyUp("w")
        pydirectinput.keyUp("a")
        pydirectinput.keyUp("s")
        pydirectinput.keyUp("d")
        pydirectinput.keyUp(pydirectinput.KEY_NUMPAD_5)
        pydirectinput.keyUp(pydirectinput.KEY_NUMPAD_8)
        pydirectinput.keyUp("shift")

    def on_play(self):
        if self.fly_plane_timer.is_active:
            pydirectinput.keyDown("w")

    def fly_plane(self):
        pydirectinput.keyDown("w")

        key_to_press = pydirectinput.KEY_NUMPAD_5 if self.direction_up else pydirectinput.KEY_NUMPAD_8
        self.logger.debug(f"Pressing num5 : {self.pressing_num5}")
        if not self.pressing_num5:
            self.logger.debug(f"Setting dur : {self.FLY_PLANE_WAVELENGTH*self.duty_cycle}")
            if self.FLY_PLANE_WAVELENGTH*self.duty_cycle != 0:
                self.fly_plane_timer.set_duration(self.FLY_PLANE_WAVELENGTH*self.duty_cycle, reset=True)
                pydirectinput.keyDown(key_to_press)
                self.pressing_num5 = True
        else: 
            self.logger.debug(f"Setting dur : {self.FLY_PLANE_WAVELENGTH*(1-self.duty_cycle)}")
            if self.FLY_PLANE_WAVELENGTH*(1-self.duty_cycle) != 0:
                self.fly_plane_timer.set_duration(self.FLY_PLANE_WAVELENGTH*(1-self.duty_cycle), reset=True)
                pydirectinput.keyUp(key_to_press)
                self.pressing_num5 = False

    def duty_cycle_up(self):
        self.logger.info(f"Increasing duty cycle from {self.duty_cycle:.2f} to {min(1, self.duty_cycle + self.DUTY_CYCLE_STEP):.2f}")
        self.duty_cycle = min(1, self.duty_cycle + self.DUTY_CYCLE_STEP)
        self.duty_cycle_var.set(f"{self.duty_cycle:.2f}")

    def duty_cycle_down(self):
        self.logger.info(f"Decreasing duty cycle from {self.duty_cycle:.2f} to {max(0, self.duty_cycle - self.DUTY_CYCLE_STEP):.2f}")
        self.duty_cycle = max(0, self.duty_cycle - self.DUTY_CYCLE_STEP)
        self.duty_cycle_var.set(f"{self.duty_cycle:.2f}")

    def toggle_dir(self):
        # release other dir key
        pydirectinput.keyUp(pydirectinput.KEY_NUMPAD_5)
        pydirectinput.keyUp(pydirectinput.KEY_NUMPAD_8)
        self.direction_up = not self.direction_up
        self.logger.info(f"New direction: {self.direction_up}")
        self.direction_var.set("Up" if self.direction_up else "Down")

    def swim(self):
        pydirectinput.keyDown("shift")

if __name__ == "__main__":
    my_autoclicker = GTAAuto()
    my_autoclicker.root.geometry("500x200+2700+-300") 
    my_autoclicker.mainloop()
 
