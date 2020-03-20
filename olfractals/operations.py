"""Helpers to manage fractal operation

A line is a list of points (2 or more) and is composed by oriented segments
defined by consecutive points.

A fractal operation convert a segment into 2 sets of lines:
- new lines where operation must recursively be applied on segments
- new lines to draw only

Operation output must be <line> or <tuple of 2 list of lines>:
    a <line> is an <array of 2-float-arrays> with at least 2 items"

We define 2 types of operations:
- Basis Operation : operation on segment ((0, 0), (1, 0))
- Generic Operation : actual fractal operation"""
import numpy as np
from functools import wraps

from .lines import BASIS_SEGMENT, assert_is_line
from .transformations import get_params, transform


# --------------------------------------------------------------------------- #
# Conversions

def gen2basis(oper_g):
    """Convert generic fractal operation into basic fractal operation"""

    @wraps(oper_g)
    def b_oper():
        return oper_g(*BASIS_SEGMENT)

    doc = oper_g.__doc__
    b_oper.__doc__ = (
        ("" if doc is None else doc)
        + "\n..about:: converted to basis operation"
    )

    return b_oper


def basis2gen(b_oper):
    """Convert basis fractal operation into generic fractal operation"""

    seg1 = BASIS_SEGMENT
    to_iter_base, to_draw_base = b_oper()

    @wraps(b_oper)
    def oper_g(p1, p2):
        seg2 = np.array([p1, p2])
        params = get_params(seg1, seg2, as_radian=True)
        to_iter = [transform(points, **params) for points in to_iter_base]
        to_draw = [transform(points, **params) for points in to_draw_base]
        return to_iter, to_draw

    oper_g.__doc__ = (
            b_oper.__doc__
            + "\n..about:: converted to generic operation"
    )

    return oper_g


# --------------------------------------------------------------------------- #
# Conversions

def operation(func):

    @wraps(func)
    def wrapped(*args, **kwargs):
        res  = func(*args, **kwargs)
        if isinstance(res, tuple):
            assert len(res) == 2, f"Got a {len(res)} item tuple instead of 2"
            to_iter, to_draw = res
            assert isinstance(to_iter, list), (
                f"Got as {type(to_iter)} as 1st item instead of list"
            )
            assert isinstance(to_draw, list), (
                f"Got as {type(to_draw)} as 2nd item instead of list"
            )
            for line in to_iter + to_draw:
                assert_is_line(line)
        elif isinstance(res, np.ndarray):
            assert_is_line(res)
            to_iter, to_draw = [res], []
        else:
            raise AssertionError(
                f"Unknown operation output type {type(res)}"
            )

        return to_iter, to_draw

    return wrapped
