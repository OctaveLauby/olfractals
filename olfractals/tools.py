""""Convenient tools for python object handling"""
import numpy as np
from time import sleep, time


def compress(lines):
    """Build reduced list of lines where consecutive lines are joined"""
    # TODO: don't only linearly browse lines
    c_lines = []
    try:
        c_line = lines[0]
    except IndexError:
        return np.array(lines)
    start, end = c_line[0], c_line[-1]
    for line in lines[1:]:
        start = line[0]
        if np.array_equal(start, end):
            c_line = np.concatenate((c_line, line[1:]))
        else:
            c_lines.append(c_line)
            c_line = line
        end = c_line[-1]
    c_lines.append(c_line)
    return np.array(c_lines)


def wait_until(predicate, freq=0.1, timeout=5, raise_err=True):
    """Wait until predicate return True"""
    start = time()
    while not predicate():
        if time() - start > timeout:
            if raise_err:
                raise TimeoutError(
                    "Predicate did not come True before timeout"
                )
            return False
        sleep(freq)
    return True


def line2seg(line):
    """Build iterable on segments defining the line (sequence of points)"""
    n = len(line)
    return (line[i:i+2] for i in range(n-1))



if __name__ == "__main__":

    l1 = np.array([[0, 1], [1, 1]])
    l2 = np.array([[1, 1], [1, 0], [2, 1]])
    lines = compress([l1, l2])
    assert len(lines) == 1
    line = lines[0]
    np.testing.assert_equal(line, [[0, 1], [1, 1], [1, 0], [2, 1]])

    line = np.array([[0, 1], [1, 1], [1, 0], [2, 1]])
    points = [[(0, 1), (1, 1)], [(1, 1), (1, 0)], [(1, 0), (2, 1)]]
    for cseg, eseg in zip(line2seg(line), points):
        np.testing.assert_equal(cseg, eseg)
