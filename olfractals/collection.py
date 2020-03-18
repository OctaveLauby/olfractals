import numpy as np

def koch_snowflake_b():
    """Basic fractal operation to draw a koch snowflake_b"""
    sin = np.sin(60 * np.pi / 180)
    line = np.array([[0, 0], [1 / 3, 0], [0.5, sin / 3], [2 / 3, 0], [1, 0]])
    return [line], []
