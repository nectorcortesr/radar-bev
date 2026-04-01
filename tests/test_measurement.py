import os
import math
import numpy as np

from src.measurement.distance import pixels_to_meters
from src.geometry.homography import compute_homography_dlt


def test_pixels_to_meters():
    """Unit test to ensure metric consistency."""
    scale_factor = 0.05
    px_dist = 100
    
    m_dist = pixels_to_meters(px_dist, scale_factor)
    
    assert math.isclose(m_dist, 5.0), f"Conversion error. Expected 5.0, got {m_dist}"