import json
from typing import List
from src.core.mapper import Point2D


class CalibrationRepository:
    """
    Maneja la persistencia de datos de calibración (lectura/escritura JSON).

    Responsabilidad única:
    - Guardar y cargar puntos de calibración desde disco
    """

    def save(self, path: str, points: List[Point2D]) -> None:
        """
        Guarda los puntos de calibración en un archivo JSON.

        Args:
            path (str): Ruta del archivo
            points (List[Point2D]): Lista de puntos a guardar
        """
        data = {"points": [[p.x, p.y] for p in points]}

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def load(self, path: str) -> List[Point2D]:
        """
        Carga puntos de calibración desde un archivo JSON.

        Args:
            path (str): Ruta del archivo

        Returns:
            List[Point2D]: Lista de puntos cargados
        """
        with open(path, "r") as f:
            data = json.load(f)

        return [Point2D(x, y) for x, y in data["points"]]
