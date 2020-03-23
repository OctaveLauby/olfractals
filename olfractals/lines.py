"""Helpers to manage lines

A line is a numpy array of points (2 float array)
"""
import numpy as np

BASIS_SEGMENT = np.array([[0, 0], [1, 0]])


# --------------------------------------------------------------------------- #
# Lines

def assert_is_line(line):
    """Check whether line is well defined"""
    assert isinstance(line, np.ndarray), "a line must be a numpy array"
    assert line.ndim == 2, "a line must be a 2d matrix (with shape=(n,2))"
    nlines, point_len = line.shape
    assert nlines > 1, "a line must contain at least 1 point"
    assert point_len == 2, "a line point must be a 2-float array"



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
    return c_lines


def line2seg(line):
    """Build iterable on segments defining the line (sequence of points)"""
    n = len(line)
    return (line[i:i+2] for i in range(n-1))


def lines2seg(lines):
    """Build iterable on segments defining the list of lines"""
    for line in lines:
        for segment in line2seg(line):
            yield segment
