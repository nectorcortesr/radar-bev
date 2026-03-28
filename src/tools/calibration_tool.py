import cv2
import numpy as np
import json
import os
from src.geometry.homography import compute_homography_dlt

points = []
CALIBRATION_FILE = "calibration.json"

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) >= 4:
            points.pop(0)

        points.append([x, y])
        print(f"Punto registrado: ({x}, {y}) - Total: {len(points)}/4")


def save_calibration(pts, filename):
    with open(filename, 'w') as f:
        json.dump({"points": pts}, f)
    print(f"Calibración guardada en {filename}")


def main():
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    cv2.rectangle(frame, (300, 300), (900, 600), (50, 50, 50), -1)
    cv2.putText(frame, "Haz clic en 4 esquinas. Presiona 'q' para salir.", 
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.namedWindow("Calibracion")
    cv2.setMouseCallback("Calibracion", mouse_callback)

    while True:
        display_frame = frame.copy()

        for i, pt in enumerate(points):
            cv2.circle(display_frame, (pt[0], pt[1]), 5, (0, 0, 255), -1)
            cv2.putText(display_frame, str(i + 1), (pt[0] + 10, pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        if len(points) == 4:
            src_pts = np.array(points, dtype=np.float32)
            dst_pts = np.array([[0, 0], [500, 0], [500, 500], [0, 500]], dtype=np.float32)

            H = compute_homography_dlt(src_pts, dst_pts)
            
            bev = cv2.warpPerspective(frame, H, (500, 500))
            cv2.imshow("Vista BEV", bev)
        
        cv2.imshow("Calibracion", display_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s') and len(points) == 4:
            save_calibration(points, CALIBRATION_FILE)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    os.makedirs("src/tools", exist_ok=True)
    main()


