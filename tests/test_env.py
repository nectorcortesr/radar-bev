def test_opencv_importable():
    import cv2
    assert cv2.__version__ is not None, "OpenCV is not installed"

def test_numpy_importable():
    import numpy as np
    assert np.__version__ is not None, "NumPy is not installed"

def test_opencv_version():
    import cv2
    major = int(cv2.__version__.split('.')[0])
    assert major >= 4, f"OpenCV 4+ is required, you have {cv2.__version__}"