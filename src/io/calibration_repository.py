import json
from typing import List
from src.core.mapper import Point2D


class CalibrationRepository:
    """
    Handles the persistence of calibration data (JSON read/write).

    Sole responsibility:
    - Save and load calibration points from disk
    """

    def save(self, path: str, points: List[Point2D]) -> None:
        """
        Saves calibration points to a JSON file.

        Args:
            path (str): File path
            points (List[Point2D]): List of points to save
        """
        data = {"points": [[p.x, p.y] for p in points]}

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def load(self, path: str) -> List[Point2D]:
        """
        Loads calibration points from a JSON file.

        Args:
            path (str): File path

        Returns:
            List[Point2D]: List of loaded points
        """
        with open(path, "r") as f:
            data = json.load(f)

        return [Point2D(x, y) for x, y in data["points"]]
