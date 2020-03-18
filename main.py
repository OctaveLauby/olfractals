"""Launch fractal drawing (WIP)"""


if __name__ == "__main__":
    import numpy as np
    from olfractals import Fractal, Screen
    from time import time


    # ---------------------------------------------------------------------- #
    # Fractal

    print("Define fractal")
    sin = np.sin(60 * np.pi / 180)
    def b_oper():
        line = np.array([[0, 0], [1/3, 0], [0.5, sin/3], [2/3, 0], [1, 0]])
        return [line], []
    iter_n = 8

    fractal = Fractal(b_oper, as_basis=True)
    for k, v in fractal.growth_info.items():
        print(f"\t| {k}={v}")
    print(f"\t| iterations={iter_n}")
    print(f"\t| segments={fractal.evaluate_growth(iter_n)}")

    # Compute fractal
    t = time()
    print("Prepare fractal lines...", end="")
    lines = fractal.compute_b(iter_n)
    line = lines[0]
    print(f" done in {time()-t}s")


    # ---------------------------------------------------------------------- #
    # Display

    screen = Screen()

    # Make points fit the screen
    t = time()
    print("Fit line...", end="")
    params = screen.compute_fit_params(line)
    print(f" done in {time()-t}s")
    for k, v in params.items():
        print(f"\t| {k}={v}")

    # Display
    t = time()
    print("Draw line...", end="")
    screen.open()
    screen.draw_line(line)
    print(f" done in {time()-t}s")

    screen.wait_close()
