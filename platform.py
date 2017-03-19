"""
==============================================
   __  __   __   _     .   ___            __
  / / / /  /  _ |_)   /_\   |   |  |\ |  /  _
 / / / /   \__| | \  /   \  |   |  | \|  \__|
/_/ /_/    L  A  B  O  R  A  T  O  R  I  E  S
==============================================

This Python file defined an optical platform

 [X]====>(=======>{+}------->[
  |      |         | \       |
===============================
||                     \     ||
||                      +->  ||
"""
from g_modles import *
import numpy as np
import logging


class Platform:
    def __init__(self, max_iteration=10):
        self.max_iteration = max_iteration
        self.devices = {}
        self.operators = []
        self.operands = []
        self.results = {}
        self.focus = None

    def add_device(self, device, pos, adapter):
        device.place(pos)
        self.devices[device] = adapter
        if device.type == 'operator':
            self.operators.append(device)
        elif device.type == 'operand':
            self.operands.append(device)
        else:
            logging.warning("Wrong input device type:", device.type)
            return None
        if not self.focus:
            self.focus = device

    def simulate(self):
        self.results.clear()
        # Simulation
        for operand in self.operands:
            res_ts = Traces(hash(operand))
            for point in operand.points:
                # Simulate each point
                traces = self.__point_sim__(point, {})
                res_ts.extend_traces(traces)
            self.results[hash(operand)] = res_ts

    def __point_sim__(self, point, points_pool, depth=0):
        if depth > self.max_iteration:
            return None
        all_results = []
        for transformer in self.operators:
            if transformer not in point.passed:
                res_points = transformer.effect(point)
                for res_point in res_points:
                    trace = Trace(hash(point))
                    trace.start(point)
                    trace.add_pos(res_point)
                    all_results.append(trace)
        return all_results


class Traces:
    def __init__(self, uid):
        self.uid = uid
        self.traces = []

    def add_trace(self, trace):
        self.traces.append(trace)

    def extend_traces(self, traces):
        self.traces.extend(traces)


class Trace:
    def __init__(self, uid):
        self.path = []
        self.uid = uid

    def start(self, point):
        self.path.clear()
        self.path.append(point)

    def add_pos(self, point):
        self.path.append(point)

    def end(self):
        return self.path[-1]

    def first(self):
        return self.path[0]


def line_end(start, angle, length):
    delta_x = length * np.cos(angle)
    delta_y = length * np.sin(angle)
    x, y = start
    return x - delta_x, y + delta_y