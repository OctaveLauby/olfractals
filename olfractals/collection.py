import numpy as np

from .operations import operation

def cos(deg):
    return np.cos(deg * np.pi / 180)


def sin(deg):
    return np.sin(deg * np.pi / 180)



class BasisOperation:

    @staticmethod
    def double_arrow():
        line = 1/4 * np.array([
            (0, 0), (0,-1), (-1, 0), (0, 1), (2, 0),
            (4, -1), (5, 0), (4, 1), (4, 0)
        ])
        return [line], []

    @staticmethod
    def double_slide():
        factor = 1/8
        line1 = np.array([(0, 0), (1/2, factor)])
        line2 = np.array([(1/2, -factor), (1,0)])
        return [line1, line2], []

    @staticmethod
    def koch_snowflake():
        """Basic fractal operation to draw a koch snowflake_b"""
        line = np.array([[0, 0], [1 / 3, 0], [0.5, sin(60) / 3], [2 / 3, 0], [1, 0]])
        return [line], []

    @staticmethod
    def spiral():
        """Basic fractal operation to draw some kind of spiral"""
        line = np.array([[0, 0], [1 / 2, 1 / 4], [1 / 2, -1 / 4], [1, 0]])
        return [line], []

    @staticmethod
    def tree():
        """"""
        trunk = 1 / 5 * np.array([(0, 0), (2, 0)])
        branch1 = 1 / 5 * np.array([(2, 0), (5, 1)])
        branch2 = 1 / 5 * np.array([(2, 0), (5, -2)])
        return [branch1, branch2], [trunk]



class StartSegment:
    vertical = [([0, 0], [0, 1])]
    horizontal = [([0, 0], [1, 0])]
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
