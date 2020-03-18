"""Launch fractal drawing (WIP)"""


if __name__ == "__main__":
    import numpy as np
    from olfractals import Fractal, Screen
    from time import time


    # ---------------------------------------------------------------------- #
    # Fractal

    from olfractals.collection import koch_snowflake_b
    fractal = Fractal(koch_snowflake_b, as_basis=True)
    iter_n = 5
    sin = np.sin(60 * np.pi / 180)
    segments = [
        ([0, 0], [0.5, sin]),
        ([0.5, sin], [1, 0]),
        ([1, 0], [0, 0]),
    ]

    print("Define fractal")
    for k, v in fractal.growth_info.items():
        print(f"\t| {k}={v}")
    print(f"\t| iterations={iter_n}")
    print(f"\t| segments={fractal.evaluate_growth(iter_n)}")

    # Compute fractal
    t = time()
    print("Prepare fractal lines...", end="")
    lines = fractal.compute_on(segments, iter_n)
    print(f" done in {time()-t}s")


    # ---------------------------------------------------------------------- #
    # Display

    screen = Screen()

    # Make points fit the screen
    t = time()
    print("Fit line...", end="")
    params = screen.compute_fit_params(np.concatenate(lines))
    print(f" done in {time()-t}s")
    for k, v in params.items():
        print(f"\t| {k}={v}")

    # Display
    t = time()
    print("Draw line...", end="")
    screen.open()
    for line in lines:
        screen.draw_line(line)
    print(f" done in {time()-t}s")

    screen.wait_close()
