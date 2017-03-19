import pygame
from platform import Platform
from g_modles.grating import Grating, GratingAdapter
from g_modles.pixels import Pixel, PixelHandler
from gui import GUI_Controller
from init import *
import numpy as np

init_all()

platform = Platform()
gratting = Grating(np.deg2rad(180), 1, 7, 11, 1.33, 'test grating')

num = 48
pixels = []
for i in range(num):
    p = Pixel(0.2, 'pixel'+str(i))
    pixels.append(p)
    platform.add_device(p, (10 + i * 0.6, -6), PixelHandler)

platform.add_device(gratting, (0, 0), GratingAdapter)

controller = GUI_Controller(platform)
controller.mainloop(1920, 1080)


