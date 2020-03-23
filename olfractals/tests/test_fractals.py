import numpy as np

from olfractals.fractal import Fractal


def test_Fractal():

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
