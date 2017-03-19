"""
=============================================
   __  __   __   _     .   ___           __
  / / / /  /  _ |_)   /_\   |   |  |\ | /  _
 / / / /   \__| | \  /   \  |   |  | \| \__|
/_/ /_/   L  A  B  O  R  A  T  O  R  I  E  S
=============================================
This Python file defined grating device
^
 \
  \      --------------------->
   \

"""
from pygame.sprite import Sprite
from .model import OpticalDevice
import numpy as np
import pygame


class Light(OpticalDevice):
    type = 'light'
    def __init__(self, source, angle):
        super().__init__('light')
        self.source = source
        self.angle = angle


class LightAdapter(Sprite):
    def __init__(self, light):
        super(LightAdapter, self).__init__()
        self.light = light
        self.dimension = 10
        self.surf = pygame.Surface
