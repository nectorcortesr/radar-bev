import numpy as np


def nullspace(A: np.ndarray) -> np.ndarray:
    """
    Calculate the zero vector of an overdetermined system Ah=0 using SVD.
    Returns the vector h of dimension (N,) that minimizes ||Ah||.
    """
    # TODO: Execute np.linalg.svd on A. Be careful with full_matrices
    U, S, Vt = None, None, None
    U, S, Vt = np.linalg.svd(A, full_matrices=False)

    # TODO: Extract the last row of Vt (which corresponds to the last column of V)
    h = None
    h = Vt[-1, :]

    return h


def least_squares_svd(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Solves Ax=b using the pseudo-inverse via SVD.
    """
    # TODO: Calculate SVD of A
    U, S, Vt = None, None, None
    U, S, Vt = np.linalg.svd(A, full_matrices=False)

    # TODO: Create the S_inv matrix (invert non-zero singular values with tolerance 1e-10)
    S_inv = np.zeros_like(S)
    for i in range(len(S)):
        if S[i] > 1e-10:
            S_inv[i] = 1 / S[i]

    # TODO: Calculate pseudo-inverse A_pinv = V @ S_inv @ U.T
    A_pinv = None
    A_pinv = Vt.T @ np.diag(S_inv) @ U.T

    # TODO: Calculate and return x = A_pinv @ b
    x = None
    x = A_pinv @ b
    return x


# --- TESTS ---
def test_nullspace():
    # Example matrix A (overdetermined system)
    A = np.random.rand(5, 4)
    # Make the last column dependent to have a real nullspace
    A[:, 3] = A[:, 0] + A[:, 1]

    h = nullspace(A)

    # Senior verification: ||Ah|| should be close to 0
    residual = np.linalg.norm(A @ h)
    assert residual < 1e-10, f"High residual error: {residual}"


def test_least_squares():
    A = np.random.rand(4, 3)
    b = np.random.rand(4)

    x_custom = least_squares_svd(A, b)
    x_numpy, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

    assert np.allclose(
        x_custom, x_numpy
    ), "Your SVD least squares does not match np.linalg.lstsq"
