"""Launch fractal drawing (WIP)"""


if __name__ == "__main__":
    import numpy as np
    from olfractals import Screen
    from time import time

    screen = Screen()
    screen.open()
    line = np.array([[0, 1], [1, 1], [1, 0], [2, 1]])

    t = time()
    print("Prepare line...", end="")
    line = np.array([[i//2, (i+1)//2] for i in range(int(1e2))])
    print(f" done in {time()-t}s")

    t = time()
    print("Fit line...", end="")
    params = screen.compute_fit_params(line)
    from pprint import pprint; pprint(params)
    print(f" done in {time()-t}s")

    t = time()
    print("Draw line...", end="")
    screen.draw_line(line)
    print(f" done in {time()-t}s")

    screen.wait_close()
