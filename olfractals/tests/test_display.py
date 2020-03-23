import numpy as np

from olfractals.display import Screen


def test_Screen():

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
