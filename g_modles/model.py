"""
==============================================
   __  __   __   _     .   ___            __
  / / / /  /  _ |_)   /_\   |   |  |\ |  /  _
 / / / /   \__| | \  /   \  |   |  | \|  \__|
/_/ /_/    L  A  B  O  R  A  T  O  R  I  E  S
==============================================

This Python file defined an super class of all optical devices
May be we will develop thermal discouragement beam.

|                                               ==|
\                                                /|
 =|-------------------------------------------->| |
/                                                \|
|                                               ==|
"""

class OpticalDevice:
    def __init__(self, o_type, name):
        self.type = o_type
        self.name = name

    def place(self, pos):
        pass

    def effect(self, point):
        pass

    def move(self, delta):
        pass


class Operator(OpticalDevice):
    def __init__(self, name):
        super().__init__('operator', name)


class Operand(OpticalDevice):
    def __init__(self, name):
        super().__init__('operand', name)
