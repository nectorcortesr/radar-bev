import cv2
import numpy as np

from typing import List

from src.core.mapper import Point2D, HomographyMapper
from src.io.calibration_repository import CalibrationRepository


class CalibrationTool:
    """
    Herramienta interactiva para seleccionar puntos y calibrar homografía.
    """

    def __init__(self, output_file: str = "calibration.json"):
        self.points: List[Point2D] = []
        self.output_file = output_file
        self.mapper = HomographyMapper()
        self.repo = CalibrationRepository()

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.points) >= 4:
                self.points.pop(0)

            self.points.append(Point2D(x, y))
            print(f"Punto: ({x}, {y}) - {len(self.points)}/4")

    def save_calibration(self):
        self.repo.save(self.output_file, self.points)
        print(f"Calibración guardada en {self.output_file}")

    def run(self):
        frame = np.zeros((720, 1280, 3), dtype=np.uint8)

        cv2.rectangle(frame, (300, 300), (900, 600), (50, 50, 50), -1)
        cv2.putText(
            frame,
            "Haz clic en 4 esquinas. 's' guardar, 'q' salir",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )

        cv2.namedWindow("Calibracion")
        cv2.setMouseCallback("Calibracion", self.mouse_callback)

        while True:
            display = frame.copy()

            for i, pt in enumerate(self.points):
                cv2.circle(display, (pt.x, pt.y), 5, (0, 0, 255), -1)
                cv2.putText(
                    display,
                    str(i + 1),
                    (pt.x + 10, pt.y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                )

            if len(self.points) == 4:
                dst = [
                    Point2D(0, 0),
                    Point2D(500, 0),
                    Point2D(500, 500),
                    Point2D(0, 500),
                ]

                success = self.mapper.calibrate(self.points, dst)

                if success:
                    bev = self.mapper.transform_frame(frame, (500, 500))
                    cv2.imshow("Vista BEV", bev)

            cv2.imshow("Calibracion", display)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
            elif key == ord("s") and len(self.points) == 4:
                self.save_calibration()

        cv2.destroyAllWindows()
