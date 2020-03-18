"""Provide a bunch of transformation

A segment is defined as 2 points (tuples)
We consider segments as oriented, so the order of these points matter
"""
import numpy as np

ORIGIN = np.array([0, 0])


def get_angle(v1, v2, as_radian=False):
    """Return angle b/w 2 angles"""
    angle = np.math.atan2(np.linalg.det([v1, v2]), np.dot(v1, v2))
    return angle if as_radian else np.degrees(angle)


def get_length(vector):
    """Return length of vector"""
    return np.linalg.norm(vector)


def to_array(arr):
    """Convert a to arr if not numpy array"""
    return arr if isinstance(arr, np.ndarray) else np.array(arr)


# --------------------------------------------------------------------------- #
# ---- Transformations


def get_params(seg1, seg2, as_radian=False):
    """Return parameters to transform seg1 into seg2"""
    seg1, seg2 = to_array(seg1), to_array(seg2)
    p11, p12 = seg1[0], seg1[1]
    p21, p22 = seg2[0], seg2[1]
    v1 = p12 - p11
    v2 = p22 - p21
    return {
        'angle': get_angle(v1, v2, as_radian=as_radian),
        'factor': get_length(v2) / get_length(v1),
        'vector': p21 - p11,
        'as_radian': as_radian,
        'origin': p11,
    }


def rot_matrix(angle, as_radian=False):
    """Return 2d rotation matrix"""
    if not as_radian:
        angle = np.radians(angle)
    cos, sin = np.cos(angle), np.sin(angle)
    return np.array([[cos, -sin], [sin, cos]])

def rotate(points, angle, origin=ORIGIN, as_radian=False):
    """Rotate points by angle relative to origin

    Args:
        points (matrix) : 2d-matrix (n*2) of points
        angle (float)   : angle of rotation (in degrees)
        origin (2-float array): point to rotate relative to
        as_radian (bool): if angle is given in radian, not degrees

    Return:
        (matrix): 2d-matrix (n*2) of rotated points
    """
    translation = np.transpose([origin])
    rotation = rot_matrix(angle, as_radian=as_radian)
    points_t = np.transpose(points)
    return np.transpose(np.dot(rotation, points_t - translation) + translation)


def scale(points, factor, origin=ORIGIN):
    """Apply hometheties b/w points and origin"""
    translation = to_array(origin)
    points = to_array(points)
    return factor * (points - translation) + translation


def transform(points, angle=None, factor=None, vector=None, origin=ORIGIN,
              as_radian=False, decimals=3):
    """Full transformation on points (rotation, homothety and translation)

    Args:
        points (matrix) : 2d-matrix (n*2) of points
        angle (float)   : angle of rotation (in degrees)
        factor (float)  : homothety factor (distance scaling)
        vector (2-float array)  : translation after other transformations
        origin (2-float array)  : origin of transformations
        as_radian (bool): if angle is given in radian, not degrees
        decimals (int)  : round transformed points
    """
    assert not (factor is None and vector is None and angle is None), (
        "Expecting at least one transformation"
    )
    points = to_array(points)
    if angle is not None:
        points = rotate(points, angle, origin=origin, as_radian=as_radian)
    if factor is not None:
        points = scale(points, factor, origin=origin)
    if vector is not None:
        vector = to_array(vector)
        points += vector
    if decimals and len(points):
        points = np.round(points, decimals)
    return points


if __name__ == "__main__":
    points = [(1, 2), (2, 2), (1, 3), (0, 2)]
    origin = points[0]
    angle = 90
    factor = 3
    vector = (-5, -10)

    # Test rotate
    rpoints = rotate(points, angle, origin=origin)
    np.testing.assert_almost_equal(rpoints, [[1, 2], [1, 3], [0, 2], [1, 1]])

    # Test scale
    spoints = scale(points, 3, origin=origin)
    np.testing.assert_almost_equal(spoints, [[1, 2], [4, 2], [1, 5], [-2, 2]])

    # Test transform
    tpoints = transform(
        points, factor=factor, angle=angle, vector=vector, origin=origin,
    )
    np.testing.assert_almost_equal(
        tpoints - vector, [[1, 2], [1, 5], [-2, 2], [1, -1]]
    )

    # Test get params
    params = get_params(points[:2], tpoints[:2])
    assert sorted(params.keys()) == [
        'angle', 'as_radian', 'factor', 'origin', 'vector'
    ]
    assert not params['as_radian']
    np.testing.assert_almost_equal(params['origin'], origin)
    a, f, v = params['angle'], params['factor'], params['vector']
    np.testing.assert_almost_equal((a, f, *v), (angle, factor, *vector))
