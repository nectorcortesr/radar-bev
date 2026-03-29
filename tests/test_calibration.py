import os
from src.io.calibration_repository import CalibrationRepository
from src.core.mapper import Point2D


def test_save_creates_file(tmp_path):
    repo = CalibrationRepository()
    file_path = tmp_path / "calib.json"

    points = [Point2D(1, 2), Point2D(3, 4)]
    repo.save(file_path, points)

    assert os.path.exists(file_path)


def test_load_returns_points(tmp_path):
    repo = CalibrationRepository()
    file_path = tmp_path / "calib.json"

    points = [Point2D(5, 6), Point2D(7, 8)]
    repo.save(file_path, points)

    loaded = repo.load(file_path)

    assert len(loaded) == 2
    assert loaded[0].x == 5
    assert loaded[0].y == 6


def test_save_and_load_consistency(tmp_path):
    repo = CalibrationRepository()
    file_path = tmp_path / "calib.json"

    original = [Point2D(10, 20), Point2D(30, 40)]
    repo.save(file_path, original)

    loaded = repo.load(file_path)

    for o, l in zip(original, loaded):
        assert o.x == l.x and o.y == l.y