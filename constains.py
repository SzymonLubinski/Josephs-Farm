from pygame import image, Color
from screeninfo import get_monitors

from pgzhelper import *

# COLORS
WATER = 96,160,168
GREEN_GRASS = 113, 143, 63
moveimage = image.load('images/bg2.png')

ORANGE = 255, 112, 8
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
REDT = 255, 0, 0, 128
GREEN = 181, 226, 77
GREENT = 181, 226, 77, 128
PURPLE = 81, 54, 170
GOLD = 255, 215, 0
BEIGE = 232, 224, 218
BROWN = 85, 53, 45

# STATIC
background = Actor('bg2')

monitor = get_monitors()[0]

FULLSCREEN_WIDTH = monitor.width
FULLSCREEN_HEIGHT = monitor.height

WIDTH = 1920
HEIGHT = 1080

BASE_WIDTH = monitor.width
BASE_HEIGHT = monitor.height
FULLSCREEN = False


def change_fullscreen():
    global FULLSCREEN
    FULLSCREEN = not FULLSCREEN


def is_fullscreen():
    return FULLSCREEN


def scale_to(objects: list, old, new):
    for obj in objects:
        obj.scale(old, new)

COLS = int(WIDTH/10)
ROWS = int(HEIGHT/10)
SPEED_GAME = 100
animals_choosing = 50
animals_speed = 0.5
tab_fs = 32
