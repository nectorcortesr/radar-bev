import numpy as np
import cv2

def to_homogeneous(points: np.ndarray) -> np.ndarray:
    """
    Convierte puntos 2D a coordenadas homogéneas.
    points shape: (N, 2) -> returns (N, 3)
    """
    # TODO: Agrega una columna de 1s a los puntos usando np.hstack o np.pad
    return np.hstack((points, np.ones((points.shape[0], 1))))

def from_homogeneous(points: np.ndarray) -> np.ndarray:
    """
    Convierte de homogéneas a 2D dividiendo por la última coordenada.
    points shape: (N, 3) -> returns (N, 2)
    """
    # TODO: Divide x e y por la coordenada z, y retorna solo x,y
    return points[:, :2] / points[:, 2][:, np.newaxis]

def translation_2d(tx: float, ty: float) -> np.ndarray:
    """Retorna matriz 3x3 de traslación"""
    # TODO: Implementar matriz T
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]])

def rotation_2d(angle_deg: float) -> np.ndarray:
    """Retorna matriz 3x3 de rotación"""
    theta = np.deg2rad(angle_deg)
    # TODO: Implementar matriz R
    return np.array([[np.cos(theta), -np.sin(theta), 0],
                     [np.sin(theta),  np.cos(theta), 0],
                     [0,              0,             1]])

def scale_2d(sx: float, sy: float) -> np.ndarray:
    """Retorna matriz 3x3 de escala"""
    # TODO: Implementar matriz S
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]])

def compose(*transforms: np.ndarray) -> np.ndarray:
    """
    Compone transformaciones.
    compose(T, R) significa aplicar R primero, luego T (T @ R)
    """
    result = np.eye(3)
    for transform in transforms:
        result = result @ transform  # <- aquí se acumula al final
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
    M = compose(T, R) # Rotar 90 deg, luego trasladar
    
    pt = np.array([[1, 0]])
    pt_hom = to_homogeneous(pt)
    
    # Aplicar matriz (M @ vector_columna)
    transformed = (M @ pt_hom.T).T
    res = from_homogeneous(transformed)
    
    # Rotar (1,0) por 90 deg da (0,1). Trasladar por (10,5) da (10,6).
    assert np.allclose(res, [[10, 6]])


