import numpy as np
import cv2

def compute_homography_dlt(pts_src, pts_dst):
    """
    Calcula la homografía H usando Direct Linear Transform (DLT).
    pts_src: array Nx2 de puntos origen
    pts_dst: array Nx2 de puntos destino
    """
    assert len(pts_src) >= 4 and len(pts_dst) >= 4, "Se necesitan al menos 4 correspondencias"

    A = []
    for i in range(len(pts_src)):
        x, y = pts_src[i][0], pts_src[i][1]
        u, v = pts_dst[i][0], pts_dst[i][1]

        A.append([-x, -y, -1, 0, 0, 0, u*x, u*y, u])
        A.append([0, 0, 0, -x, -y, -1, v*x, v*y, v])
        
    A = np.array(A)

    U, S, Vt = np.linalg.svd(A)
    h = Vt[-1, :]

    H = h.reshape(3, 3)

    return H / H[2, 2]

if __name__ == "__main__":

    src = np.array([[0, 0], [100, 0], [100, 100], [0, 100]], dtype=np.float32)
    dst = np.array([[10, 20], [80, 20], [90, 90], [5, 80]], dtype=np.float32)

    H_dlt = compute_homography_dlt(src, dst)
    H_cv2, _ = cv2.findHomography(src, dst)

    error = np.max(np.abs(H_dlt - (H_cv2 / H_cv2[2, 2])))
    print(f"Error máximo contra OpenCV: {error}")

    assert error < 1e-6, "Bug detectado: tu DLT no coincide con la implementación industrial"
    print("¡Módulo DLT implementado exitosamente!")