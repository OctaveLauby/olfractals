import numpy as np


def cos(deg):
    return np.cos(deg * np.pi / 180)


def sin(deg):
    return np.sin(deg * np.pi / 180)


class BasisOperation:

    @staticmethod
    def koch_snowflake_b():
        """Basic fractal operation to draw a koch snowflake_b"""
        line = np.array([[0, 0], [1 / 3, 0], [0.5, sin(60) / 3], [2 / 3, 0], [1, 0]])
        return [line], []

    @staticmethod
    def spiral_b():
        """Basic fractal operation to draw some kind of spiral"""
        line = np.array([[0, 0], [1 / 2, 1 / 4], [1 / 2, -1 / 4], [1, 0]])
        return [line], []


class StartSegment:
    vertical = [([0, 0], [1, 0])]
    horizontal = [([0, 0], [0, 1])]
    triangle = [
        ([0, 0], [cos(60), sin(60)]),
        ([cos(60), sin(60)], [1, 0]),
        ([1, 0], [0, 0]),
    ]
    star_3 = [
        ([0, 0], [0, 1]),
        ([0, 0], [cos(210), sin(210)]),
        ([0, 0], [cos(330), sin(330)]),
    ]
    star_5 = [
        ([0, 0], [cos(72 *i), sin(72 *i)])
        for i in range(5)
    ]
