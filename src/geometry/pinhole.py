import numpy as np


def project_points(
    X_world: np.ndarray, K: np.ndarray, R: np.ndarray, t: np.ndarray
) -> np.ndarray:
    """
    Proyecta puntos 3D a coordenadas de píxeles 2D usando el modelo Pinhole.
    X_world: array Nx3 con puntos 3D
    """
    num_points = X_world.shape[0]

    # Por qué coordenadas homogéneas: Permite usar álgebra lineal simple (multiplicación)
    # para aplicar rotación y traslación simultáneamente en un solo paso matricial.
    # TODO: Convierte X_world a coordenadas homogéneas (Nx4) añadiendo una columna de unos.
    # Pista: np.ones y np.hstack
    X_hom = np.hstack((X_world, np.ones((num_points, 1))))

    # TODO: Construye la matriz extrínseca de 3x4 concatenando R (3x3) y t (3x1).
    # Pista: np.hstack
    extrinsic = np.hstack((R, t))
    # Multiplicación matricial: K (3x3) @ extrinsic (3x4) @ X_hom.T (4xN) -> (3xN)
    # Transponemos al final para volver a (Nx3)
    x_cam = (K @ extrinsic @ X_hom.T).T

    # Por qué dividir por Z: Es la división de perspectiva. Hace que los objetos
    # lejanos converjan en el punto de fuga en nuestra imagen 2D.
    # TODO: Divide la primera columna (X) y segunda (Y) por la tercera columna (Z).
    u = x_cam[:, 0] / x_cam[:, 2]
    v = x_cam[:, 1] / x_cam[:, 2]

    return np.column_stack((u, v))


if __name__ == "__main__":
    # Matriz K simulada (Cámara industrial típica)
    K_intrinsic = np.array([[800.0, 0.0, 960.0], [0.0, 800.0, 540.0], [0.0, 0.0, 1.0]])

    # Identidad: cámara en el origen mirando hacia adelante
    R_ext = np.eye(3)
    # Traslación: cámara a 10 metros de altura mirando un contenedor
    t_ext = np.array([[0], [10], [0]])

    # 4 esquinas de un contenedor minero (X, Y, Z) en metros
    contenedor_3d = np.array([[-2, 0, 10], [2, 0, 10], [2, 0, 20], [-2, 0, 20]])

    pixels = project_points(contenedor_3d, K_intrinsic, R_ext, t_ext)
    print("Píxeles proyectados:\n", pixels)

    # Assert de verificación obligatoria
    expected_first_pixel = np.array([800.0, 1340.0])
    error = np.linalg.norm(pixels[0] - expected_first_pixel)
    assert error < 0.01, f"Error geométrico alto: {error}. Revisa tu álgebra matricial."
    print("Proyección exitosa, error numérico en tolerancia.")
