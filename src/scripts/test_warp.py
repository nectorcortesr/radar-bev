import cv2
from src.geometry.transforms2d import rotation_2d, scale_2d, compose


def test_warp_image():
    img = cv2.imread("data/yard.png")
    assert img is not None, "Imagen no encontrada"

    h, w = img.shape[:2]

    R = rotation_2d(30)
    S = scale_2d(0.5, 0.5)
    M = compose(R, S)

    M_cv = M[:2, :]
    warped = cv2.warpAffine(img, M_cv, (w, h))

    cv2.imwrite("data/yard_warped.jpg", warped)

    assert warped.shape[0] == h and warped.shape[1] == w
