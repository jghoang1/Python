import random
import pyautogui
import pydirectinput
import time

COLUMNS = 8
MINHEIGHT = 150
MINWIDTH = 300

COLOR_ON = "#88FF88"
COLOR_OFF = "#FF8888"
COLOR_ON_INACTIVE = "#80b080"
COLOR_OFF_INACTIVE = "#a07070"
COLOR_DEBOUNCE = "#e7eb7f"

FRAMERATE = 50
FRAMELENGTH = 1000 // 50
DEFAULT_DELAY = 0.10 # seconds


def move_and_click(self, x, y, max_dx = 10, max_dy = 10, pause_after = 0.5):
    duration = random.uniform(0.3, 1.5)
    dx = random.randrange(-max_dx, max_dx)
    dy = random.randrange(-max_dy, max_dy)
    # tween = random.choice((pyautogui.easeInQuad,
    #                         pyautogui.easeOutQuad,
    #                         pyautogui.easeInOutQuad,
    #                         pyautogui.easeInElastic))
    pyautogui.moveTo(x + dx, y + dy, duration=duration, tween = pyautogui.easeInOutQuad)
    pydirectinput.click(x + dx, y + dy, clicks = 1)
    time.sleep(pause_after)