""""Convenient tools for python object handling"""
from time import sleep, time


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
    import numpy as np
    line = np.array([[0, 1], [1, 1], [1, 0], [2, 1]])
    points = [[(0, 1), (1, 1)], [(1, 1), (1, 0)], [(1, 0), (2, 1)]]

    for cseg, eseg in zip(line2seg(line), points):
        np.testing.assert_equal(cseg, eseg)
