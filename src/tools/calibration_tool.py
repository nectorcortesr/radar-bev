import cv2
import numpy as np
from typing import List
import json

from src.core.mapper import Point2D, HomographyMapper
from src.io.calibration_repository import CalibrationRepository


class CalibrationTool:
    """
    Headless calibration tool:
    - Saves base frame
    - Uses points from calibration.json
    - Validates homography
    """

    def __init__(self, output_file: str = "calibration.json"):
        self.output_file = output_file
        self.mapper = HomographyMapper()
        self.repo = CalibrationRepository()

    def run(self):
        # 1. Create base frame (or load real image)
        frame = np.zeros((720, 1280, 3), dtype=np.uint8)

        cv2.rectangle(frame, (300, 300), (900, 600), (50, 50, 50), -1)

        # 2. Save image for manual calibration
        cv2.imwrite("calibration_frame.jpg", frame)
        print("Frame saved as calibration_frame.jpg")

        # 3. Load points from JSON
        try:
            with open(self.output_file, "r") as f:
                data = json.load(f)
                points = data["points"]
        except Exception:
            print("calibration.json does not exist or is malformed")
            print("Create the file manually with 4 points")
            return

        if len(points) != 4:
            print("Exactly 4 points are required")
            return

        src_pts = [Point2D(x, y) for x, y in points]

        dst_pts = [
            Point2D(0, 0),
            Point2D(500, 0),
            Point2D(500, 500),
            Point2D(0, 500),
        ]

        # 4. Calibrate homography
        success = self.mapper.calibrate(src_pts, dst_pts)

        if not success:
            print("Error calculating homography")
            return

        # 5. Validation: generate BEV and save it
        bev = self.mapper.transform_frame(frame, (500, 500))
        cv2.imwrite("bev_debug.jpg", bev)

        print("Calibration OK")
        print("bev_debug.jpg generated for validation")