import cv2
import numpy as np
import math
import csv
import os
from datetime import datetime

SCALE_FACTOR = 0.05
ALERT_THRESHOLD_M = 10.0


def get_centroids(mask):
    """Encuentra contornos y calcula sus centroides usando momentos."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centroids = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 100:
            continue

        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroids.append((cx, cy))
    return centroids


def log_event(filename, dist_m):
    """Escribe una nueva fila en el CSV con el timestamp y la distancia."""
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), round(dist_m, 2)])


def main():
    frame = np.zeros((600, 600, 3), dtype=np.uint8)
    cv2.rectangle(frame, (100, 100), (150, 150), (0, 255, 255), -1)
    cv2.rectangle(frame, (180, 150), (230, 200), (0, 255, 255), -1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    centroids = get_centroids(mask)

    if len(centroids) == 2:
        c1, c2 = centroids[0], centroids[1]
        cv2.circle(frame, c1, 5, (0, 0, 255), -1)
        cv2.circle(frame, c2, 5, (0, 0, 255), -1)

        cv2.line(frame, c1, c2, (255, 0, 0), 2)

        px_dist = math.hypot(c2[0] - c1[0], c2[1] - c1[1])
        m_dist = px_dist * SCALE_FACTOR

        cv2.putText(
            frame,
            f"{m_dist:.2f}m",
            ((c1[0] + c2[0]) // 2, (c1[1] + c2[1]) // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        if m_dist < ALERT_THRESHOLD_M:
            log_event("events.csv", m_dist)
            print(f"¡ALERTA! Vehículos demasiado cerca: {m_dist:.2f}m.")

    cv2.imshow("HSV Tracker", frame)
    cv2.imshow("Mascara HSV", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    assert os.path.exists(
        "events.csv"
    ), "Error: El archivo events.csv no se creó en el sistema."
    print("Test de segmentación y logging: VERDE")


if __name__ == "__main__":
    os.makedirs("src/detection", exist_ok=True)
    main()
