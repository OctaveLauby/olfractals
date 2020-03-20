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

from .lines import BASIS_SEGMENT, compress, lines2seg
from .operations import basis2gen, gen2basis
from .transformations import get_params, transform


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
            0: ([BASIS_SEGMENT], []),
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

    # ----------------------------------------------------------------------- #
    # Computation

    def build_cache(self, n):
        """Build cache up to iteration n"""
        try:
            return self.cache[n]
        except KeyError:
            pass

        to_iter_b, to_draw_b = self.cache[1]            # base iteration
        to_iter_p, to_draw_p = self.build_cache(n-1)    # previous iteration

        # Apply previous iteration to each to-iter segment of base iteration
        to_iter, to_draw = [], list(to_draw_p)
        for seg_b in lines2seg(to_iter_b):
            params = get_params(BASIS_SEGMENT, seg_b, as_radian=True)
            for line_p in to_iter_p:
                to_iter.append(transform(line_p, **params))
            for line_p in to_draw_p:
                to_draw.append(transform(line_p, **params))

        result = compress(to_iter), compress(to_draw)
        self.cache[n] = result
        return result

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

        to_iter, to_draw = self.build_cache(n)
        if concat:
            if len(to_iter) and len(to_draw):
                return to_iter + to_draw
            else:
                return to_iter
        else:
            return to_iter, to_draw

    def compute_on(self, segments, n):
        """Compute n iterations of basic fractal operation

        Args:
            segments (list): list of segments (2-float-tuple)
            n (int): number of iteration to compute

        Return:
            (list): list of lines to draw
        """
        b_lines = self.compute_b(n, concat=True)
        lines = []
        for segment in segments:
            params = get_params(BASIS_SEGMENT, segment, as_radian=True)
            for line in b_lines:
                lines.append(transform(line, **params))
        return compress(lines)


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
