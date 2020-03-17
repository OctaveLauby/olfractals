"""Launch fractal drawing (WIP)"""


if __name__ == "__main__":
    import numpy as np
    from olfractals import Screen

    screen = Screen()
    screen.open()
    line = np.array([[0, 1], [1, 1], [1, 0], [2, 1]])
    screen.compute_fit_params(line)
    screen.draw_line(line)
    screen.wait_close()
