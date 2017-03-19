"""
=============================================
   __  __   __   _     .   ___           __
  / / / /  /  _ |_)   /_\   |   |  |\ | /  _
 / / / /   \__| | \  /   \  |   |  | \| \__|
/_/ /_/   L  A  B  O  R  A  T  O  R  I  E  S
=============================================
"""
from pygame.locals import *
import numpy as np
from g_modles.grating import GratingAdapter
from g_modles.pixels import PixelHandler
from gif import GIFImage
import pygame
import logging
import time

class GUI_Controller:
    def __init__(self, platform):
        self.adapters = {}
        self.platform = platform
        self.running = True
        self.event = None
        self.show_lights = True
        self.focus = None
        self.scale = 1
        self.__width__ = 40
        self.show_current_lights = True
        self.show_all_lights = False
        self.current_selection = platform.operands

    def mainloop(self, width=1920, height=1080, movie='logo2.gif'):
        pygame.init()
        screen = pygame.display.set_mode((width, height), FULLSCREEN)
        logging.info("Create a new window.")
        # Startup animation
        # movie = pygame.movie.Movie(movie)
        start_time = time.time()
        gif = GIFImage(movie)
        running = True
        while time.time() - start_time < 3.5 and running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
            gif.render(screen, (400, 0))
            pygame.display.update()

        self.color_picker = Colorchanger()
        self.canvas = pygame.Surface((3 * width, 3 * height))
        self.canvas_rect = self.canvas.get_rect()
        self.base = [-width, -height]
        self.center = (round(1.5 * width), round(1.5 * height))
        self.width = width
        self.height = height
        while self.running:
            # Check for events
            for event in pygame.event.get():
                self.events_handler(event)
            # Simulate and update
            self.platform.simulate()
            # Draw
            self.canvas.fill(0xffffff)
            self.draw_grid()
            self.focus = self.platform.focus
            self.devices = self.platform.devices
            for device in self.devices:
                adp = self.devices[device](device, (self.length_converter, self.axis_converter, self.reverse_converter))
                if device == self.focus:
                    adp.update(pygame.key.get_pressed())
                adp.draw()
                axis_x, axis_y = adp.axis
                drag_x, drag_y = adp.drag_point
                base_x, base_y = self.center
                self.canvas.blit(adp.surf, (base_x + axis_x - drag_x, base_y - axis_y - drag_y))

            self.results = self.platform.results
            size = len(self.platform.results)
            for operand in self.platform.results:
                # print(len(self.results[operand].traces))
                line_color = self.color_picker.next(size)
                for trace in self.results[operand].traces:
                    if self.show_all_lights or (self.show_current_lights and operand == hash(self.platform.focus)):
                        # Render trace
                        path = []
                        if len(trace.path) < 2:
                            continue
                        for i in range(len(trace.path)):
                            path.append(self.aaxis_converter(trace.path[i].pos))
                        tail = path[1:]
                        line = iter(zip(path, tail))
                        for start, end in line:
                            # print(start, end)
                            pygame.draw.aaline(self.canvas, line_color, start, end)
                    base = trace.end()
                    base = self.aaxis_converter(base.pos)
                    rect = (base[0] - 4, base[1] - 4, 8, 8)
                    pygame.draw.rect(self.canvas, line_color, rect, 4)

            screen.blit(self.canvas, self.base)
            pygame.display.update()
            pygame.time.Clock().tick(60)

    def events_handler(self, event):
        handle_dict = {
            K_F2: self.create_handler,
            K_q: self.sel_handler,
            K_e: self.sel_handler,
            K_DELETE: self.del_handler,
            K_UP: self.move_camera_handler,
            K_DOWN: self.move_camera_handler,
            K_LEFT: self.move_camera_handler,
            K_RIGHT: self.move_camera_handler,
            K_EQUALS: self.scale_handler,
            K_MINUS: self.scale_handler,
            K_F3: self.show_light_handler,
            K_F4: self.show_light_handler
        }
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.running = False
            else:
                self.event = event
                handle_dict.get(event.key, self.fake_pass)()
        elif event.type == QUIT:
            self.running = False
        else:
            pass

    def create_handler(self):
        pass

    def del_handler(self):
        pass

    def sel_handler(self):
        if self.event.key == K_q:
            if self.platform.focus in self.current_selection:
                pos = self.current_selection.index(self.platform.focus)
                index = (pos + 1) % len(self.current_selection)
                self.platform.focus = self.current_selection[index]
            elif len(self.current_selection) > 0:
                self.platform.focus = self.current_selection[0]
            else:
                self.platform.focus = None
        elif self.event.key == K_e:
            if self.current_selection == self.platform.operands:
                self.current_selection = self.platform.operators
            elif self.current_selection == self.platform.operators:
                self.current_selection = self.platform.operands
            else:
                logging.critical("Selection error!")
        else:
            pass

    def show_light_handler(self):
        if self.event.key == K_F3:
            self.show_current_lights = not self.show_current_lights
        elif self.event.key == K_F4:
            self.show_all_lights = not self.show_all_lights
        else:
            logging.error("Wrong command")

    def scale_handler(self):
        if self.event.key == K_EQUALS and pygame.key.get_mods() & KMOD_SHIFT:
            if self.scale < 2:
                self.scale += 0.25
        elif self.event.key == K_MINUS:
            if self.scale > 0.25:
                self.scale -= 0.25
        else:
            logging.error("Wrong command")

    def move_camera_handler(self):
        if self.event.key == K_UP:
            if pygame.key.get_mods() & KMOD_SHIFT:
                self.base[1] += 5
            else:
                self.base[1] += 100
        elif self.event.key == K_DOWN:
            if pygame.key.get_mods() & KMOD_SHIFT:
                self.base[1] -= 5
            else:
                self.base[1] -= 100
        elif self.event.key == K_LEFT:
            if pygame.key.get_mods() & KMOD_SHIFT:
                self.base[0] += 5
            else:
                self.base[0] += 100
        elif self.event.key == K_RIGHT:
            if pygame.key.get_mods() & KMOD_SHIFT:
                self.base[0] -= 5
            else:
                self.base[0] -= 100
        else:
            logging.error("Wrong moving camera command")
            return None
        return True

    def add_device(self, device):
        pass

    def fake_pass(self):
        pass

    def axis_converter(self, axis):
        pixel_axis = list(map(self.length_converter, axis))
        # for _ in range(len(self.center)):
        #     pixel_axis[_] += self.center[_]
        return tuple(pixel_axis)

    def aaxis_converter(self, axis):
        pixel_axis = list(map(self.length_converter, axis))
        pixel_axis[0] = self.center[0] + pixel_axis[0]
        pixel_axis[1] = self.center[1] - pixel_axis[1]
        return tuple(pixel_axis)

    def length_converter(self, length):
        pixels_pre_cm = self.scale * self.__width__
        return round(pixels_pre_cm * length)

    def reverse_converter(self, pixels):
        pixels_pre_cm = self.scale * self.width
        return pixels / pixels_pre_cm

    def draw_grid(self):
        step = 2 *  self.scale * self.__width__
        for i in range(int(3 * self.height / step) + 1):
            pygame.draw.aaline(self.canvas, (136, 124, 124), (0, self.center[1] + i * step),
                               (3 * self.width, self.center[1] + i * step))
            pygame.draw.aaline(self.canvas, (136, 124, 124), (0, self.center[1] - i * step),
                               (3 * self.width, self.center[1] - i * step))

        for i in range(int(3 * self.width / step) + 1):
            pygame.draw.aaline(self.canvas, (136, 124, 124), (self.center[0] + i * step, 0),
                               (self.center[0] + i * step, 3 * self.height))
            pygame.draw.aaline(self.canvas, (136, 124, 124), (self.center[0] - i * step, 0),
                               (self.center[0] - i * step, 3 * self.height))
        # pygame.draw.line(self.canvas, 0xaf0aff, (0, self.center[1]), (self.width * 3, self.center[1]), 3)
        # pygame.draw.line(self.canvas, 0xaf0aff, (self.center[0], 0), (self.center[0], self.height * 3), 3)

class Colorchanger:
    def __init__(self):
        self.colors = [(0xFF, 0, 0), (0xFF, 0xD7, 0), (0, 0xFF, 0xFF), (0, 0x33, 0x66),
                       (0, 0, 0x80), (0xE3, 0x23, 0x26), (0, 0xFF, 0x80), (0xFF, 0x24, 0), (0xFF, 0xFF, 00)]
        self.index = 0
        self.cycle = 0

    def next(self, size):
        if self.cycle % 2 == 0:
            self.index += 1
            self.index %= size
            # self.index %= len(self.colors)
            self.index %= 3
        self.cycle += 1
        return self.colors[self.index]