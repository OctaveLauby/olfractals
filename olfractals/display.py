import numpy as np
import pygame
from threading import Thread

from .lines import line2seg
from .tools import wait_until
from .transformations import transform

COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
}


class Screen(object):

    def __init__(self, size=(700, 700), name=None, line_params=None,
                 fps=20):
        """Initiate a Screen object"""

        # Screen parameters
        self.name = "FractalDisplay" if name is None else name
        self.screen = None
        self.size = size
        self.background = COLORS['white']

        # Refresh params
        self.initiated = False
        self.stop = False
        self.thread = None
        self.fps = fps
        self.clock = pygame.time.Clock()

        # Line drawing params
        self.line_params = {
            'color': COLORS['black'],
            'width': 2,
        }
        if line_params:
            self.line_params.update(line_params)

        # Line drawing fitting
        self.fit_params = None

    def open(self):
        """Open a screen"""
        self.thread = Thread(target=self.refresh)
        self.thread.start()
        wait_until(lambda: self.initiated)

    def wait_close(self):
        """Wait for screen to be closed"""
        self.thread.join()
        self.thread = None

    # ----------------------------------------------------------------------- #
    # Refresh management

    def clean(self):
        """Clean what is on screen"""
        self.screen.fill(self.background )

    def refresh(self):
        """Keep the screen updated"""
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.name)
        self.clean()
        self.initiated = True

        self.stop = False
        while not self.stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop = True
            self.update()
            self.clock.tick(self.fps)
        self.screen = None
        pygame.quit()
        self.initiated = False

    def update(self):
        """Update display"""
        pygame.display.flip()

    # ----------------------------------------------------------------------- #
    # Drawing

    def draw_line(self, line, fit=True, **params):
        """Draw line on screen"""
        if fit: line = self.fit_transform(line)

        for p1, p2 in line2seg(line):
            self.draw_segment(p1, p2, fit=False, **params)

    def draw_segment(self, p1, p2, fit=True, color=None, width=1):
        """Draw segment b/w 2 points"""
        assert self.screen is not None, "Can't draw line if no screen opened"
        if fit: p1, p2 = self.fit_transform([p1, p2])

        color = self.line_params['color'] if color is None else color
        width = self.line_params['width'] if width is None else width
        pygame.draw.line(self.screen, color, p1, p2, width)

    # ----------------------------------------------------------------------- #
    # Drawing - Fitting

    def compute_fit_params(self, points, screen_ratio=0.8):
        """Compute fit params

        Args:
            points (matrix): points to fit in screen
            screen_ratio (matrix):
        """
        # TODO: Add a mirror symmetry to reverse image
        # # Required cause top of screen is at y=0

        # Compute rectangle containing all points
        x_min, x_max, y_min, y_max = np.inf, -np.inf, np.inf, -np.inf
        for x, y in points:
            if x < x_min: x_min = x
            if y < y_min: y_min = y
            if x > x_max: x_max = x
            if y > y_max: y_max = y
        p_center = np.array([(x_min+x_max)/2, (y_min+y_max)/2])
        p_xdelta = x_max - x_min
        p_ydelta = y_max - y_min

        # Compute rectangle where to display points
        dx, dy = self.size[0], self.size[1]
        d_center = np.array([dx/2, dy/2])
        d_xdelta = screen_ratio * dx
        d_ydelta = screen_ratio * dy

        # Compute parameters to move points in display rect
        params = {
            'origin': p_center,
            'factor': min(d_xdelta/p_xdelta, d_ydelta/p_ydelta),
            'vector': d_center - p_center,
        }
        self.fit_params = dict(params)
        return params

    def fit_transform(self, points):
        """Apply transform on using computed fit_params"""
        if self.fit_params is None:
            return points
        return transform(points, **self.fit_params)


if __name__ == "__main__":
    screen = Screen()
    line = np.array([[0, 1], [1, 1], [1, 0], [2, 1]])

    # Compute params to nicely  fit line in screen
    params = screen.compute_fit_params(line)
    assert sorted(params.keys()) == ['factor', 'origin', 'vector']
    assert params['factor'] == 280.0
    np.testing.assert_almost_equal(params['origin'], np.array([1. , 0.5]))
    np.testing.assert_almost_equal(params['vector'], np.array([349. , 349.5]))\

    # Check transformation
    np.testing.assert_almost_equal(
        screen.fit_transform(line),
        [[ 70., 490.], [350., 490.], [350., 210.], [630., 490.]],
    )
