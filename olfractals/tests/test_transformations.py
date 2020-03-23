import numpy as np

import olfractals.transformations as lib


def test_all():
    points = [(1, 2), (2, 2), (1, 3), (0, 2)]
    origin = points[0]
    angle = 90
    factor = 3
    vector = (-5, -10)

    # Test rotate
    rpoints = lib.rotate(points, angle, origin=origin)
    np.testing.assert_almost_equal(rpoints, [[1, 2], [1, 3], [0, 2], [1, 1]])

    # Test scale
    spoints = lib.scale(points, 3, origin=origin)
    np.testing.assert_almost_equal(spoints, [[1, 2], [4, 2], [1, 5], [-2, 2]])

    # Test transform
    tpoints = lib.transform(
        points, factor=factor, angle=angle, vector=vector, origin=origin,
    )
    np.testing.assert_almost_equal(
        tpoints - vector, [[1, 2], [1, 5], [-2, 2], [1, -1]]
    )

    # Test get params
    params = lib.get_params(points[:2], tpoints[:2])
    assert sorted(params.keys()) == [
        'angle', 'as_radian', 'factor', 'origin', 'vector'
    ]
    assert not params['as_radian']
    np.testing.assert_almost_equal(params['origin'], origin)
    a, f, v = params['angle'], params['factor'], params['vector']
    np.testing.assert_almost_equal((a, f, *v), (angle, factor, *vector))
