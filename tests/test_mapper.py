from src.core.mapper import HomographyMapper, Point2D
import numpy as np

def test_calibration_success():
    mapper = HomographyMapper()

    src = [Point2D(0,0), Point2D(1,0), Point2D(1,1), Point2D(0,1)]
    dst = [Point2D(0,0), Point2D(2,0), Point2D(2,2), Point2D(0,2)]

    assert mapper.calibrate(src, dst)
    assert mapper.H is not None

def test_measure_distance():
    mapper = HomographyMapper(scale_factor=0.1)
    p1 = Point2D(0,0)
    p2 = Point2D(10,0)

    assert mapper.measure_distance(p1, p2) == 1.0

def test_measure_distance_zero():
    mapper = HomographyMapper(scale_factor=0.1)
    p = Point2D(10, 10)

    assert mapper.measure_distance(p, p) == 0.0


def test_measure_distance_positive():
    mapper = HomographyMapper(scale_factor=0.1)
    p1 = Point2D(0, 0)
    p2 = Point2D(10, 0)

    assert mapper.measure_distance(p1, p2) > 0


def test_calibrate_returns_true():
    mapper = HomographyMapper()

    src = [Point2D(0,0), Point2D(1,0), Point2D(1,1), Point2D(0,1)]
    dst = [Point2D(0,0), Point2D(2,0), Point2D(2,2), Point2D(0,2)]

    assert mapper.calibrate(src, dst)