import math
import cv2
import numpy as np
import os


def pixels_to_meters(px_distance, scale_factor):
    """Converts distance in pixels to meters."""
    return px_distance * scale_factor


def test_pixels_to_meters():
    dist = pixels_to_meters(100, 0.025)
    assert math.isclose(dist, 2.5), f"Numerical error: {dist} != 2.5"
    print("Unit test pixels_to_meters: GREEN")


measurement_points = []
SCALE_FACTOR = 0.05


def measure_callback(event, x, y, flags, param):
    global measurement_points
    if event == cv2.EVENT_LBUTTONDOWN:
        measurement_points.append((x, y))
        if len(measurement_points) > 2:
            measurement_points = [(x, y)]


def main():
    test_pixels_to_meters()

    bev_frame = np.zeros((600, 600, 3), dtype=np.uint8)
    cv2.putText(
        bev_frame,
        "Click on 2 points to measure. 'q' to quit.",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (200, 200, 200),
        1,
    )

    cv2.namedWindow("BEV Measurement")
    cv2.setMouseCallback("BEV Measurement", measure_callback)

    while True:
        display = bev_frame.copy()

        # Render clicks
        for pt in measurement_points:
            cv2.circle(display, pt, 5, (0, 0, 255), -1)

        if len(measurement_points) == 2:
            p1, p2 = measurement_points[0], measurement_points[1]

            cv2.line(display, p1, p2, (0, 255, 0), 2)

            px_dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])

            m_dist = pixels_to_meters(px_dist, SCALE_FACTOR)

            mid_point = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
            cv2.putText(
                display,
                f"{m_dist:.2f} m",
                mid_point,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2,
            )

        cv2.imwrite("measurement_bev.jpg", display)

if __name__ == "__main__":
    os.makedirs("src/measurement", exist_ok=True)
    main()
