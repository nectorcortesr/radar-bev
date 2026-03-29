import cv2
import numpy as np
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Point2D:
    """Representa un punto coordenado en 2D."""

    x: int
    y: int


class HomographyMapper:
    """
    Abstrae la transformación de perspectiva y medición métrica.
    """

    def __init__(self, scale_factor: float = 0.05):
        self.H: Optional[np.ndarray] = None
        self.scale_factor: float = scale_factor

    def calibrate(self, src_pts: List[Point2D], dst_pts: List[Point2D]) -> bool:
        """
        Calcula la matriz H a partir de 4 puntos de referencia.

        Args:
            src_pts: Lista de 4 puntos origen en la imagen de la cámara.
            dst_pts: Lista de 4 puntos destino en la vista BEV.

        Returns:
            bool: True si la calibración fue exitosa y la matriz es válida.
        """
        src = np.array([[pt.x, pt.y] for pt in src_pts], dtype=np.float32)
        dst = np.array([[pt.x, pt.y] for pt in dst_pts], dtype=np.float32)

        self.H, _ = cv2.findHomography(src, dst)

        return self.H is not None

    def transform_frame(
        self, frame: np.ndarray, output_size: Tuple[int, int]
    ) -> np.ndarray:
        """
        Aplica la transformación de perspectiva al frame.
        """
        assert self.H is not None, "Debes calibrar antes de transformar el frame."

        return cv2.warpPerspective(frame, self.H, output_size)

    def measure_distance(self, pt1: Point2D, pt2: Point2D) -> float:
        """
        Calcula la distancia en metros reales entre dos puntos BEV.
        """
        px_dist = math.hypot(pt2.x - pt1.x, pt2.y - pt1.y)

        return px_dist * self.scale_factor
