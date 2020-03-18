"""Launch fractal drawing (WIP)"""


if __name__ == "__main__":
    import numpy as np
    from olfractals import Fractal, Screen
    from time import time


    # ---------------------------------------------------------------------- #
    # Fractal

    from olfractals.collection import koch_snowflake_b

    print("Define fractal")
    iter_n = 5
    fractal = Fractal(koch_snowflake_b, as_basis=True)
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
