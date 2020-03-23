import numpy as np

import olfractals.lines as lib


def test_all():

    l1 = np.array([[0, 1], [1, 1]])
    l2 = np.array([[1, 1], [1, 0], [2, 1]])
    lib.assert_is_line(l1)
    lib.assert_is_line(l2)
    lines = lib.compress([l1, l2])
    assert len(lines) == 1
    line = lines[0]
    np.testing.assert_equal(line, [[0, 1], [1, 1], [1, 0], [2, 1]])

    line = np.array([[0, 1], [1, 1], [1, 0], [2, 1]])
    points = [[(0, 1), (1, 1)], [(1, 1), (1, 0)], [(1, 0), (2, 1)]]
    for cseg, eseg in zip(lib.line2seg(line), points):
        np.testing.assert_equal(cseg, eseg)