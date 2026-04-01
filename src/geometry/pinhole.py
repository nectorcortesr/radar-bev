import numpy as np


def project_points(
    X_world: np.ndarray, K: np.ndarray, R: np.ndarray, t: np.ndarray
) -> np.ndarray:
    """
    Projects 3D points to 2D pixel coordinates using the Pinhole model.
    X_world: Nx3 array with 3D points
    K: 3x3 intrinsic matrix
    R: 3x3 rotation matrix
    t: 3x1 translation vector
    """
    num_points = X_world.shape[0]

    # Why homogeneous coordinates: Allows using simple linear algebra (multiplication)
    # to apply rotation and translation simultaneously in a single matrix step.
    # TODO: Convert X_world to homogeneous coordinates (Nx4) by adding a column of ones.
    # Hint: np.ones and np.hstack
    X_hom = np.hstack((X_world, np.ones((num_points, 1))))

    # TODO: Construct the 3x4 extrinsic matrix by concatenating R (3x3) and t (3x1).
    # Hint: np.hstack
    extrinsic = np.hstack((R, t))
    # atrix multiplication: K (3x3) @ extrinsic (3x4) @ X_hom.T (4xN) -> (3xN)
    # Transpose at the end to get back to (Nx3)
    x_cam = (K @ extrinsic @ X_hom.T).T

    # Why divide by Z: It's perspective division. It makes objects
    # far away converge to the vanishing point in our 2D image.
    # TODO: Divide the first column (X) and second (Y) by the third column (Z).
    u = x_cam[:, 0] / x_cam[:, 2]
    v = x_cam[:, 1] / x_cam[:, 2]

    return np.column_stack((u, v))


if __name__ == "__main__":
    # Simulated K matrix (Typical industrial camera)
    K_intrinsic = np.array([[800.0, 0.0, 960.0], [0.0, 800.0, 540.0], [0.0, 0.0, 1.0]])

    # Identity: camera at the origin looking forward
    R_ext = np.eye(3)
    # Translation: camera 10 meters high looking at a container
    t_ext = np.array([[0], [10], [0]])

    # 4 corners of a mining container (X, Y, Z) in meters
    container_3d = np.array([[-2, 0, 10], [2, 0, 10], [2, 0, 20], [-2, 0, 20]])

    pixels = project_points(container_3d, K_intrinsic, R_ext, t_ext)
    print("Projected pixels:\n", pixels)
    # Mandatory verification assert
    expected_first_pixel = np.array([800.0, 1340.0])
    error = np.linalg.norm(pixels[0] - expected_first_pixel)
    assert error < 0.01, f"High geometric error: {error}. Check your matrix algebra."
    print("Projection successful, numerical error within tolerance.")