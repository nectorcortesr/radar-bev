import numpy as np


def nullspace(A: np.ndarray) -> np.ndarray:
    """
    Calcula el vector nulo de un sistema sobredeterminado Ah=0 usando SVD.
    Retorna el vector h de dimension (N,) que minimiza ||Ah||.
    """
    # TODO: Ejecutar np.linalg.svd sobre A. Ojo con full_matrices
    U, S, Vt = None, None, None
    U, S, Vt = np.linalg.svd(A, full_matrices=False)

    # TODO: Extraer la última fila de Vt (que corresponde a la última columna de V)
    h = None
    h = Vt[-1, :]

    return h


def least_squares_svd(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Resuelve Ax=b usando la pseudo-inversa via SVD.
    """
    # TODO: Calcular SVD de A
    U, S, Vt = None, None, None
    U, S, Vt = np.linalg.svd(A, full_matrices=False)

    # TODO: Crear la matriz S_inv (invertir los valores singulares no nulos con tolerancia 1e-10)
    S_inv = np.zeros_like(S)
    for i in range(len(S)):
        if S[i] > 1e-10:
            S_inv[i] = 1 / S[i]

    # TODO: Calcular pseudo-inversa A_pinv = V @ S_inv @ U.T
    A_pinv = None
    A_pinv = Vt.T @ np.diag(S_inv) @ U.T

    # TODO: Calcular y retornar x = A_pinv @ b
    x = None
    x = A_pinv @ b
    return x


# --- TESTS ---
def test_nullspace():
    # Matriz A de ejemplo (sistema sobredeterminado)
    A = np.random.rand(5, 4)
    # Hacemos que la última columna sea dependiente para tener un nullspace real
    A[:, 3] = A[:, 0] + A[:, 1]

    h = nullspace(A)

    # Verificación Senior: ||Ah|| debe ser casi 0
    residual = np.linalg.norm(A @ h)
    assert residual < 1e-10, f"Error residual muy alto: {residual}"


def test_least_squares():
    A = np.random.rand(4, 3)
    b = np.random.rand(4)

    x_custom = least_squares_svd(A, b)
    x_numpy, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

    assert np.allclose(
        x_custom, x_numpy
    ), "Tu SVD least squares no coincide con np.linalg.lstsq"
