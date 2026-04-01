import numpy as np


def to_homogeneous(points: np.ndarray) -> np.ndarray:
    """
    Converts 2D points to homogeneous coordinates.
    points shape: (N, 2) -> returns (N, 3)
    """
    # TODO: Add a column of 1s to the points using np.hstack or np.pad
    return np.hstack((points, np.ones((points.shape[0], 1))))


def from_homogeneous(points: np.ndarray) -> np.ndarray:
    """
    Converts from homogeneous to 2D by dividing by the last coordinate.
    points shape: (N, 3) -> returns (N, 2)
    """
    # TODO: Divide x and y by the z coordinate, and return only x, y
    return points[:, :2] / points[:, 2][:, np.newaxis]


def translation_2d(tx: float, ty: float) -> np.ndarray:
    """Returns 3x3 translation matrix"""
    # TODO: Implement translation matrix
    return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])


def rotation_2d(angle_deg: float) -> np.ndarray:
    """Returns 3x3 rotation matrix"""
    theta = np.deg2rad(angle_deg)
    # TODO: Implement rotation matrix
    return np.array(
        [
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1],
        ]
    )


def scale_2d(sx: float, sy: float) -> np.ndarray:
    """Returns 3x3 scaling matrix"""
    # TODO: Implement scaling matrix
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])


def compose(*transforms: np.ndarray) -> np.ndarray:
    """
    Composes transformations.
    compose(T, R) means apply R first, then T (T @ R)
    """
    result = np.eye(3)
    for transform in transforms:
        result = result @ transform  # <- here it accumulates at the end
    return result


# --- TESTS ---
def test_homogeneous():
    pts = np.array([[10, 20]])
    hom = to_homogeneous(pts)
    assert np.allclose(hom, [[10, 20, 1]])
    assert np.allclose(from_homogeneous(hom), pts)


def test_transforms():
    T = translation_2d(10, 5)
    R = rotation_2d(90)
    M = compose(T, R)  # Rotate 90 deg, then translate

    pt = np.array([[1, 0]])
    pt_hom = to_homogeneous(pt)

    # Apply matrix (M @ column_vector)
    transformed = (M @ pt_hom.T).T
    res = from_homogeneous(transformed)

    # Rotate (1,0) by 90 deg gives (0,1). Translate by (10,5) gives (10,6).
    assert np.allclose(res, [[10, 6]])
