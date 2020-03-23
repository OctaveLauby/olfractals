"""Launch fractal drawing (WIP)"""


if __name__ == "__main__":
    import numpy as np
    from olfractals import Fractal, Screen, MAX_ITER
    from olfractals.collection import BasisOperation, StartSegment
    from time import time


    # ---------------------------------------------------------------------- #
    # Params

    func = BasisOperation.dragon
    params = {
        'elbow_x': 3 / 5,
        'elbow_y': 2 / 5,
    }
    segments = StartSegment.horizontal
    iter_n = MAX_ITER


    # ---------------------------------------------------------------------- #
    # Fractal

    fractal = Fractal(
        BasisOperation.configured(func, **params),
        as_basis=True,
    )
    iter_n = fractal.max_iter(1e5) if iter_n is MAX_ITER  else iter_n

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
