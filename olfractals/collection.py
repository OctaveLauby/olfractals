import numpy as np
from copy import deepcopy
from functools import wraps


def cos(deg):
    return np.cos(deg * np.pi / 180)


def sin(deg):
    return np.sin(deg * np.pi / 180)



class BasisOperation:

    @classmethod
    def configured(cls, mthd=None, **params):
        """Return method working with given default parameters"""

        if isinstance(mthd, str):
            try:
                mthd = getattr(cls, mthd)
            except AttributeError:
                raise ValueError(
                    f"Unknown basic operation name '{mthd}'"
                    f", make sure to use a mthd name from {cls.__name__}"

                )

        @wraps(mthd)
        def wrapped(*args, **kwargs):
            parameters = deepcopy(params)
            parameters.update(kwargs)
            return mthd(*args, **parameters)

        doc = "" if mthd.__doc__ is None else mthd.__doc__
        wrapped.__doc__ = doc + (
            f"\n..about:: following default values are modified: {params}"
        )

        return wrapped

    @staticmethod
    def double_arrow():
        """Basic fractal operation to draw a """
        line = 1/4 * np.array([
            (0, 0), (0,-1), (-1, 0), (0, 1), (2, 0),
            (4, -1), (5, 0), (4, 1), (4, 0)
        ])
        return [line], []

    @staticmethod
    def dragon(elbow_x=1/2, elbow_y=1/2):
        """Basic fractal operation to draw a dragon

        Good params to try:
            elbow_x=3/5, elbow_y=2/5
        """
        elbow = [elbow_x, elbow_y]
        line1 = np.array([[0, 0], elbow])
        line2 = np.array([[1, 0], elbow])
        return [line1, line2], []

    @staticmethod
    def eve_dragon():
        """Basic fractal operation to draw eve dragon"""
        line1 = np.array([[0, 0], [0, 1/2], [1/2, 0]])
        line2 = np.array([[1, 0], [1/2, 0]])
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
    def leaf():
        """Basic fractal operation to draw a leaf"""
        trunk = 1 / 5 * np.array([(0, 0), (2, 0)])

        bases = []
        leafs = []
        origin = trunk[1]
        for vector in  1/5 * np.array([(1, 2), (3, 1), (2, -2)]):
            sep = origin + 1/3 * vector
            bases.append(np.array([origin, sep]))
            leafs.append(np.array([sep, origin + vector]))
        return leafs, [trunk] + bases


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
