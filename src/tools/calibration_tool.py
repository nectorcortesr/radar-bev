import cv2
import numpy as np
from typing import List
import json

from src.core.mapper import Point2D, HomographyMapper
from src.io.calibration_repository import CalibrationRepository


class CalibrationTool:
    """
    Herramienta HEADLESS para calibración:
    - Guarda frame base
    - Usa puntos desde calibration.json
    - Valida homografía
    """

    def __init__(self, output_file: str = "calibration.json"):
        self.output_file = output_file
        self.mapper = HomographyMapper()
        self.repo = CalibrationRepository()

    def run(self):
        # 1. Crear frame base (o cargar imagen real)
        frame = np.zeros((720, 1280, 3), dtype=np.uint8)

        cv2.rectangle(frame, (300, 300), (900, 600), (50, 50, 50), -1)

        # 2. Guardar imagen para calibrar manualmente
        cv2.imwrite("calibration_frame.jpg", frame)
        print("Frame guardado como calibration_frame.jpg")

        # 3. Cargar puntos desde JSON
        try:
            with open(self.output_file, "r") as f:
                data = json.load(f)
                points = data["points"]
        except Exception:
            print("No existe calibration.json o está mal formado")
            print("Crea el archivo manualmente con 4 puntos")
            return

        if len(points) != 4:
            print("Se necesitan exactamente 4 puntos")
            return

        src_pts = [Point2D(x, y) for x, y in points]

        dst_pts = [
            Point2D(0, 0),
            Point2D(500, 0),
            Point2D(500, 500),
            Point2D(0, 500),
        ]

        # 4. Calibrar homografía
        success = self.mapper.calibrate(src_pts, dst_pts)

        if not success:
            print("Error al calcular homografía")
            return

        # 5. Validación: generar BEV y guardarlo
        bev = self.mapper.transform_frame(frame, (500, 500))
        cv2.imwrite("bev_debug.jpg", bev)

        print("Calibración OK")
        print("Se generó bev_debug.jpg para validación")