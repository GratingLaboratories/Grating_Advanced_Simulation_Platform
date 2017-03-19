"""
==============================================
   __  __   __   _     .   ___            __
  / / / /  /  _ |_)   /_\   |   |  |\ |  /  _
 / / / /   \__| | \  /   \  |   |  | \|  \__|
/_/ /_/    L  A  B  O  R  A  T  O  R  I  E  S
==============================================

This Python file defined monitor device

==<RGB RGB RGB RGB RGB RGB RGB RGB RGB RGB>==

"""

from .model import Operand
from .point import Point
from pygame.sprite import Sprite
from pygame.locals import *
import pygame


class Pixel(Operand):
    def __init__(self, width, name):
        super().__init__(name)
        self.width = width
        self.points = []
        self.axis = None

    def place(self, pos):
        self.axis = list(pos)
        self.points.clear()
        for i in range(3):
            point = Point((pos[0] + i * self.width, pos[1]), 'real', 1)
            self.points.append(point)

    def move(self, delta):
        assert len(delta) >= 2
        self.axis[0] += delta[0]
        self.axis[1] += delta[1]
        self.points.clear()
        for i in range(3):
            point = Point((self.axis[0] + i * self.width, self.axis[1]), 'real', 1)
            self.points.append(point)

    def __hash__(self):
        temp_str = self.name + str(self.width)
        return hash(temp_str)


class PixelHandler(Sprite):
    def __init__(self, pixel, converters):
        super(PixelHandler, self).__init__()
        self.pixel = pixel
        l_converter, a_converter, r_converter = converters

        self.axis = a_converter(pixel.axis)
        self.l_converter = l_converter
        self.a_converter = a_converter
        self.r_converter = r_converter
        self.drag_point = (0, 0)
        self.width = l_converter(pixel.width)

        self.surf = pygame.Surface((self.width * 3 + 30, 30))
        self.surf.fill(0xff0000)
        self.surf.set_colorkey(0xff0000)
        self.rect = self.surf.get_rect()

    def draw(self):
        base_x, base_y = self.drag_point
        pygame.draw.rect(self.surf, 0xff0101, (base_x, base_y, self.width, self.width), int(self.width / 1.5))
        base_x += self.width
        pygame.draw.rect(self.surf, 0x00ff00, (base_x, base_y, self.width, self.width), int(self.width / 1.5))
        base_x += self.width
        pygame.draw.rect(self.surf, 0x0000ff, (base_x, base_y, self.width, self.width), int(self.width / 1.5))

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.pixel.move((0, self.r_converter(10)))
            else:
                self.pixel.move((0, self.r_converter(200)))
        if pressed_keys[K_s]:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.pixel.move((0, self.r_converter(-10)))
            else:
                self.pixel.move((0, self.r_converter(-200)))
        if pressed_keys[K_a]:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.pixel.move((self.r_converter(-10), 0))
            else:
                self.pixel.move((self.r_converter(-200), 0))
        if pressed_keys[K_d]:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.pixel.move((self.r_converter(10), 0))
            else:
                self.pixel.move((self.r_converter(200), 0))
        self.axis = self.a_converter(self.pixel.axis)


def dpc_calculator(resolution, size, ratio):
    import math

    width, height = resolution
    r_w, r_h = ratio
    length_w = size * r_w / math.sqrt(r_w ** 2 + r_h ** 2)
    length_w_cm = length_w * 2.54
    return width / length_w_cm
