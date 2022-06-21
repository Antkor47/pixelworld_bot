import pyautogui
import time

sand = "sand.png"
left = 870, 500, 80, 80

below = 927, 566, 80, 80

pixel_below = 960, 605

def check_block(png, direction):
    block = pyautogui.locateOnScreen(png, region=(927, 566, 80, 80), confidence=0.5)
    if block:
        return 1
    else:
        return 0

def check_pixel_below():
    pixel = pyautogui.pixel(960, 605)
    print(pixel)
    return [pixel[0], pixel[1], pixel[2]]
