import tkinter as tk
import tkinter.ttk as ttk

import pyautogui
import logging

# root = tk.Tk()

# frm = ttk.Frame(root, padding=10)

# frm.grid()

# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

# root.mainloop()

logging.basicConfig(level=logging.DEBUG)

COLUMNS = 3


class AutoClicker():

    STANDARD_BUTTONS = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
    ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
    'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
    'alt', 'altleft', 'altright', 'backspace', 'capslock', 'ctrl', 'ctrlleft', 'ctrlright', 'delete',
    'down', 'end', 'enter', 'esc', 'escape', 'f1', 'f10',
    'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
    'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    'final', 'fn', 'help', 'home', 'insert',  
    'left', 'modechange', 'multiply',
    'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
    'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
    'pgup', 'print', 'printscreen', 'return', 'right', 'scrolllock',
    'shift', 'shiftleft', 'shiftright', 'space', 'subtract', 'tab',
    'up', 'win', 'winleft', 'winright', 'command', 'option', 'optionleft', 'optionright']

    def __init__(self):
        self.root = tk.Tk()
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()

        ttk.Label(self.frm, text="An Autoclicker").grid(column=0, row=0, columnspan=COLUMNS)
        ttk.Label(self.frm, text="by Julius\n").grid(column=0, row=1, columnspan=COLUMNS)

        self.label_mouse_pos = ttk.Label(self.frm, text="Mouse Position: ")

        self.label_mouse_pos.grid(column=0, row=2, sticky="w", columnspan=COLUMNS)


    def press_release_key(self, key):
        logging.info("Callback reached for key: {}".format(key))
        button = [button for button in self.buttons if button["text"] == key][0]

        if key in self.pressed_keys:
            pyautogui.keyUp(key)
            self.pressed_keys.remove(key) 
        else:
            pyautogui.keyDown(key)
            self.pressed_keys.append(key)
        self._update_pressed_keys_label()
        
    def _update_pressed_keys_label(self):
        self.pressed_keys_label.config(text="Pressed buttons: " + ", ".join(self.pressed_keys))


    def add_button(self, key, column, row):
        button = ttk.Button(self.frm, text=key, command=lambda:self.press_release_key(key))
        button.grid(column=column, row=row)
        self.buttons.append(button)
    

    def mainloop(self):
        self.root.mainloop()


class TestClicker(AutoClicker):
    BUTTONS = ['w', 'a', 's', 'd',
    'down', 'left', 'right', 'up', 
    'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
    'num7', 'num8', 'num9', 
    'shift', 'space',]
    
    def __init__(self):
        super().__init__()
        for i in range(len(self.BUTTONS)):
            self.add_button(self.BUTTONS[i], column=i%COLUMNS, row=3+i//COLUMNS)


    

if __name__ == "__main__":
    my_autoclicker = TestClicker()
    my_autoclicker.mainloop()
