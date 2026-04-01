import cv2
import numpy as np
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Point2D:
    """It represents a coordinate point in 2D."""

    x: int
    y: int


class HomographyMapper:
    """
    Abstracts the perspective transformation and metric measurement.
    """

    def __init__(self, scale_factor: float = 0.05):
        self.H: Optional[np.ndarray] = None
        self.scale_factor: float = scale_factor

    def calibrate(self, src_pts: List[Point2D], dst_pts: List[Point2D]) -> bool:
        """
        Calculates the H matrix from 4 reference points.

        Args:
            src_pts: List of 4 source points in the camera image.
            dst_pts: List of 4 destination points in the BEV view.
        Returns:
            bool: True if the calibration was successful and the matrix is valid.
        """
        src = np.array([[pt.x, pt.y] for pt in src_pts], dtype=np.float32)
        dst = np.array([[pt.x, pt.y] for pt in dst_pts], dtype=np.float32)

        self.H, _ = cv2.findHomography(src, dst)

        return self.H is not None

    def transform_frame(
        self, frame: np.ndarray, output_size: Tuple[int, int]
    ) -> np.ndarray:
        """
        Applies the perspective transformation to theframe.
        """
        assert self.H is not None, "You must calibrate before transforming the frame."

        return cv2.warpPerspective(frame, self.H, output_size)

    def measure_distance(self, pt1: Point2D, pt2: Point2D) -> float:
        """
        Calculates the real-world distance in meters between two BEV points.
        """
        px_dist = math.hypot(pt2.x - pt1.x, pt2.y - pt1.y)

        return px_dist * self.scale_factor
