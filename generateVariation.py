# from IPython.display import display, HTML
# from ipywidgets import interact, interactive, fixed, interact_manual
# import ipywidgets as widgets
# from ipywidgets import *
# import pandas as pd
# from pyautogui import sleep
# pd.set_option('display.max_colwidth', None)
import warnings
warnings.filterwarnings('ignore')
# import string
from PIL import Image
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
import numpy as np
# import math
import random


def changePic(r2,g2,b2,a2, l):

    r = ((l[0] + ((r2 / 255 * 2) - 1) * 255 * l[0] / l[0]).astype(int))
    g = ((l[1] + ((g2 / 255 * 2) - 1) * 255 * l[1] / l[1]).astype(int))
    b = ((l[2] + ((b2 / 255 * 2) - 1) * 255 * l[2] / l[2]).astype(int))
    a = ((l[3] + ((a2 / 255 * 2) - 1) * 255 * l[3] / l[3]).astype(int))
    
    r[r > 255] = 255
    g[g > 255] = 255
    b[b > 255] = 255
    a[a > 255] = 255

    r[r < 0] = 0
    g[g < 0] = 0
    b[b < 0] = 0
    a[a < 0] = 0
    
    new[..., 0] = r
    new[..., 1] = g
    new[..., 2] = b
    new[..., 3] = a

    return new

def makeRandomImage(pngFileName):
    # sets the image and variables
    im = Image.open(pngFileName).convert('RGBA')
    im.load()
    original = np.array(im)

    # removes the head of the pickaxe
    original[(original != [(73, 54, 21, 255)]).any(axis=2) &
    (original != [(40, 30, 11, 255)]).any(axis=2) &
    (original != [(137, 103, 39, 255)]).any(axis=2) &
    (original != [(104, 78, 30, 255)]).any(axis=2) &
    (original != [(0, 0, 0, 0)]).any(axis=2)
    ] = 0

    # removes the handle of the pickaxe
    cropped = np.array(im)
    handle = original
    original = cropped - original
    original[(original == [(0, 0, 0, 0)]).any(axis=2)] = original[(original == [(0, 0, 0, 0)]).any(axis=2)] * 0.5
    r, g, b, a = np.rollaxis(original, axis=-1)
    global new
    new = np.empty_like(cropped)

    new[..., 0] = r
    new[..., 1] = g
    new[..., 2] = b
    new[..., 3] = a

    na2 = new

    l = np.rollaxis(na2, axis=-1)
    new = np.empty_like(na2)
    a = 255
    with open("words.txt", "r") as f:
        words = f.read().split(" ")

    # randomizes the stats of the pickaxe
    p1 = uses = random.randint(100, 2000)
    p2 = attack = random.randint(2, 15)
    p3 = speed = random.randint(5, 20)
    p4 = attackDamageBonus = random.randint(1, 5)
    p5 = attackSpeedBonus = random.randint(1, 5)
    p6 = enchantmentValue = random.randint(1, 5)

    # changes the color of the pickaxe by randomizing the rgb values
    r = random.randint(10, 220)
    g = random.randint(10, 220)
    b = random.randint(10, 220)

    # apply the changes to the pickaxe and save it
    a1 = Image.fromarray(handle + changePic(r, g, b, a, l))
    a1.convert('P').save(f'pics/PickaxeItem+{random.choice(words).capitalize()}+ITEMS+0+{p1}+{p2}+{p3}+{p4}+{p5}+{p6}+NEEDS_IRON_TOOL+Items.STICK+tab(CreativeModeTab.TAB_TOOLS).png')

    # example of output:
    # PickaxeItem+pickaxe_name+ITEMS+0+0+0+0+0+0+0+NEEDS_IRON_TOOL+Items.STICK+tab(CreativeModeTab.TAB_TOOLS)'stacksTo(64)

