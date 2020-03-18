"""Helpers to manage fractal operation

A line is a list of points (2 or more) and is composed by oriented segments
defined by consecutive points.

A fractal operation convert a segment into 2 sets of lines:
- new lines where operation must recursively be applied on segments
- new lines to draw only

We define 2 types of operations:
- Basis Operation : operation on segment ((0, 0), (1, 0))
- Generic Operation : actual fractal operation
"""
import numpy as np
from functools import wraps

from .tools import compress, line2seg
from .transformations import get_params, transform


# --------------------------------------------------------------------------- #
# Conversions

def gen2basis(oper_g):
    """Convert generic fractal operation into basic fractal operation"""

    @wraps(oper_g)
    def b_oper():
        return oper_g((0, 0), (1, 0))

    doc = oper_g.__doc__
    b_oper.__doc__ = (
        ("" if doc is None else doc)
        + "\n..about:: converted to basis operation"
    )

    return b_oper


def basis2gen(b_oper):
    """Convert basis fractal operation into generic fractal operation"""

    seg1 = np.array([[0, 0], [1, 0]])
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
# Fractal class

class SafetyError(Exception):
    """Exception raised when fractal computation might take too long"""

class Fractal(object):

    def __init__(self, func, as_basis=False):
        """Initiate a fractal instance

        Args:
            func (callable): fractal operation
            as_basis (bool): whether operation is basis
        """
        self.b_func = func if as_basis else gen2basis(func)
        self._g_func = None if as_basis else func
        self.cache = {
            # iteration (int): (list of to-iter lines, list of to-draw lines)
            0: (np.array([[[0, 0], [0, 1]]]), np.array([])),
            1: self.b_func(),
        }

        self.growth_info = {}
        self._compute_info()


    @property
    def g_func(self):
        if self._g_func is None:
            self._g_func = basis2gen(self.b_func)
        return self._g_func

    @property
    def q(self):
        return self.growth_info['rate']

    @property
    def r(self):
        return self.growth_info['rest']

    @property
    def basis_output(self):
        return self.cache[1]

    # ----------------------------------------------------------------------- #
    # Computation information

    def _compute_info(self):
        """Evaluate space complexity of basic fractal operation

        Proof:
            q               is the nb of segments to split after 1 operation
            r               is the nb of segments to keep as it is after 1 operation
            Si              is the nb of segments to split after iteration i
            Ki              is the nb of segments to keep as it is after iteration i
            Ui = Si + Ki    is the nb of segments after iteration i

            Si+1 = q.Si             => Sn = q^n.S0
            Ki+1 = r.Si + Ki        => Kn = r.q^(n-1).S0 + K0

            For S0=1, K0=0          Un = q^n + r * q^(n-1)
        """
        # Compute number of segments to iter on and draw only
        to_iter, to_draw = self.basis_output
        self.growth_info['rate'] = sum([len(points)-1 for points in to_iter])
        self.growth_info['rest'] = sum([len(points)-1 for points in to_draw])

    def evaluate_growth(self, n):
        """Return number of segments after n iterations"""
        return self.q**n + self.r*(self.q**(n-1))


    def compute_b(self, n, max_segments=1e7, concat=True):
        """Compute n iterations of basic fractal operation

        Args:
            n (int): number of iteration to compute
            max_segments (int): max number of segments allowed for computation
                1e7 is the limit where transformation computation and drawing
                start to take too much time (10s for matrix transformation and
                30s for drawing on decent machine)
            concat (bool): concatenate all lines

        Return:
            (matrix) if concat
            (2-matrix-tuple) if not concat
        """
        if max_segments and self.evaluate_growth(n) > max_segments:
            raise SafetyError(
                f"Computing {n} iteration(s) will create more than"
                f" {max_segments} segments"
            )

        basis_seg = np.array([(0, 0), (1, 0)])
        if n <= 0:
            return np.array([basis_seg]), np.array([])

        to_iter_b, to_draw_b = self.basis_output
        to_iter, to_draw = to_iter_b, to_draw_b
        for i in range(n-1):
            to_iter_new = []
            for line in to_iter:
                segments = line2seg(line)
                for segment in segments:
                    params = get_params(basis_seg, segment, as_radian=True)
                    for l in to_iter_b:
                        to_iter_new.append(transform(l, **params))
                    for l in to_draw_b:
                        to_draw.append(transform(l, **params))
            to_iter = compress(to_iter_new)
            to_draw = compress(to_draw)

        if compress:
            if len(to_iter) and len(to_draw):
                return np.concatenate(to_iter, to_draw)
            else:
                return to_iter
        else:
            return to_iter, to_draw


if __name__ == "__main__":

    sin = np.sin(60 * np.pi / 180)

    def b_oper():
        line = np.array([[0, 0], [0.5, sin], [1, 0]])
        return [line], []

    fractal = Fractal(b_oper, as_basis=True)
    assert fractal.growth_info == {'rate': 2, 'rest': 0}
    lines = fractal.compute_b(2)
    assert len(lines) == 1
    np.testing.assert_equal(lines[0], [
        [0., 0.], [-0.5, 0.866], [0.5, 0.866], [1.5, 0.866], [1., 0.]
    ])
