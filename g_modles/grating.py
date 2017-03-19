"""
==============================================
   __  __   __   _     .   ___            __
  / / / /  /  _ |_)   /_\   |   |  |\ |  /  _
 / / / /   \__| | \  /   \  |   |  | \|  \__|
/_/ /_/    L  A  B  O  R  A  T  O  R  I  E  S
==============================================

This Python file defined grating device
| | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | |
"""

from .model import Operator
from .point import Point
from platform import line_end
from pygame.sprite import Sprite
from pygame.locals import *
import numpy as np
import pygame
import time


class Grating(Operator):
    def __init__(self, angle, radius, thickness, number, r_index, name):
        super().__init__(name)
        self.platform = None
        self.angle = angle
        self.radius = radius
        self.thickness = thickness
        self.number = number
        self.r_index = r_index
        self.axis = None
        self.depth = np.cos(self.angle / 2) * self.radius
        self.half_gap = np.sin(self.angle / 2) * self.radius

    def place(self, pos):  # all in cm
        base_x, base_y = pos
        gap = self.half_gap * 2
        self.axis = list(pos)
        self.centers = [(base_x + self.half_gap + gap * _, base_y - self.depth) for _ in range(self.number)]

    def effect(self, point):
        res = []
        # print(self.centers)
        for center in self.centers:
            center_x, center_y = center
            src_x, src_y = point.pos
            # Check angle
            angle = np.arctan((center_x - src_x) / (center_y - src_y))
            if np.abs(angle) > self.angle / 2:
                continue
            angle = np.deg2rad(90) + angle
            u_len = np.sqrt((center_x - src_x) ** 2 + (center_y - src_y) ** 2)
            reverse_v = (self.r_index - 1) / self.radius - self.r_index / u_len
            v_len = 1 / reverse_v
            if v_len > 0:
                p_type = 'real'
            else:
                p_type = 'fake'

            target = line_end(point.pos, angle, u_len + v_len)
            p = Point(target, p_type, 1)
            # point.passed.append(self)
            res.append(p)
        return tuple(res)

    def move(self, delta):
        assert len(delta) >= 2
        self.axis[0] += delta[0]
        self.axis[1] += delta[1]
        base_x, base_y = self.axis
        gap = self.half_gap * 2
        self.centers = [(base_x + self.half_gap + gap * _, base_y - self.depth) for _ in range(self.number)]

    def __hash__(self):
        temp_str = self.name + str(self.thickness) + str(self.number) + str(self.angle) + str(self.radius)
        return hash(temp_str)


class GratingAdapter(Sprite):
    def __init__(self, grating, converters):
        super(GratingAdapter, self).__init__()
        self.grating = grating
        l_converter, a_converter, r_converter = converters

        self.l_converter = l_converter
        self.a_converter = a_converter
        self.r_converter = r_converter

        self.axis = a_converter(grating.axis)
        self.angle = grating.angle
        self.number = grating.number
        self.radius = l_converter(grating.radius)
        self.top = l_converter(grating.radius - grating.depth)
        self.depth = l_converter(grating.depth)
        self.gap = l_converter(np.sin(grating.angle / 2) * grating.radius)

        self.height = l_converter(grating.thickness) + self.top
        self.width = 2 * self.gap * grating.number
        self.drag_point = (10, self.top + 30)
        self.centers = []
        for i in range(self.number):
            self.centers.append((int(self.drag_point[0] + self.gap * (2 * i + 1)), int(self.drag_point[1] + self.depth)))

        self.surf = pygame.Surface((self.width + 50, self.height + 100))
        self.surf.fill(0xff0000)
        self.surf.set_colorkey(0xff0000)

    def draw(self, width=3, angle=0):
        base = list(self.drag_point)
        pygame.draw.line(self.surf, (0, 0, 0), base, (base[0], base[1] + self.height), width)
        base = (base[0], base[1] + self.height)

        pygame.draw.line(self.surf, (0, 0, 0), base, (base[0] + self.width, base[1]), width)
        base = (base[0] + self.width, base[1])

        pygame.draw.line(self.surf, (0, 0, 0), base, (base[0], base[1] - self.height), width)
        for center in self.centers:
            rect = (center[0] - self.radius, center[1] - self.radius, 2 * self.radius, 2 * self.radius)
            pygame.draw.arc(self.surf, 0x000000, rect, np.deg2rad(90) - self.angle / 2,
                            np.deg2rad(90) + self.angle / 2, width)
            rect = (center[0] - 2, center[1] - 2, 4, 4)
            pygame.draw.rect(self.surf, 0x000000, rect, 4)

    def update(self, pressed_keys):
        small_step = 10
        large_step = 200
        if pressed_keys[K_w]:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.grating.move((0, self.r_converter(small_step)))
            else:
                self.grating.move((0, self.r_converter(large_step)))
        if pressed_keys[K_s]:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.grating.move((0, self.r_converter(-small_step)))
            else:
                self.grating.move((0, self.r_converter(-large_step)))
        if pressed_keys[K_a]:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.grating.move((self.r_converter(-small_step), 0))
            else:
                self.grating.move((self.r_converter(-large_step), 0))
        if pressed_keys[K_d]:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.grating.move((self.r_converter(small_step), 0))
            else:
                self.grating.move((self.r_converter(large_step), 0))
        self.axis = self.a_converter(self.grating.axis)