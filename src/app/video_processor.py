import cv2
import time
import json
import numpy as np

from src.core.mapper import HomographyMapper, Point2D
from src.detection.hsv_tracker import get_centroids


class VideoProcessor:
    def __init__(self, video_path: str, calibration_file="calibration.json"):
        self.video_path = video_path
        self.mapper = HomographyMapper()

        with open(calibration_file, "r") as f:
            pts = json.load(f)["points"]

        src_pts = [Point2D(x, y) for x, y in pts]
        dst_pts = [
            Point2D(0, 0),
            Point2D(500, 0),
            Point2D(500, 500),
            Point2D(0, 500),
        ]

        self.mapper.calibrate(src_pts, dst_pts)

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        assert cap.isOpened()

        # -------- VIDEO WRITER --------
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (500, 500))

        # -------- EVENT LOG --------
        import csv
        csv_file = open("events.csv", "w", newline="")
        writer = csv.writer(csv_file)
        writer.writerow(["frame", "min_distance_m", "alert"])

        prev_time = time.time()
        frame_id = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_id += 1

            # ---------- DETECCIÓN HSV ----------
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower = np.array([20, 100, 100])
            upper = np.array([30, 255, 255])
            mask = cv2.inRange(hsv, lower, upper)
            centroids = get_centroids(mask)

            # ---------- BEV ----------
            bev = self.mapper.transform_frame(frame, (500, 500))
            bev_points = []

            for cx, cy in centroids:
                pt = np.array([[[cx, cy]]], dtype=np.float32)
                warped = cv2.perspectiveTransform(pt, self.mapper.H)
                x_bev, y_bev = warped[0][0]

                bev_points.append(Point2D(int(x_bev), int(y_bev)))
                cv2.circle(bev, (int(x_bev), int(y_bev)), 5, (0, 0, 255), -1)

            # ---------- DISTANCIA ----------
            min_dist = float("inf")
            closest_pair = None

            for i in range(len(bev_points)):
                for j in range(i + 1, len(bev_points)):
                    d = self.mapper.measure_distance(bev_points[i], bev_points[j])
                    if d < min_dist:
                        min_dist = d
                        closest_pair = (bev_points[i], bev_points[j])

            alert = 0

            if closest_pair:
                p1, p2 = closest_pair

                cv2.line(bev, (p1.x, p1.y), (p2.x, p2.y), (255, 0, 0), 2)

                mid = ((p1.x + p2.x) // 2, (p1.y + p2.y) // 2)

                cv2.putText(
                    bev,
                    f"{min_dist:.2f} m",
                    mid,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2,
                )

                if min_dist < 10:
                    alert = 1
                    cv2.putText(
                        bev,
                        "ALERTA!",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (0, 0, 255),
                        3,
                    )

            # ---------- FPS ----------
            current_time = time.time()
            fps = 1.0 / max(current_time - prev_time, 1e-9)
            prev_time = current_time

            cv2.putText(
                bev,
                f"FPS: {fps:.1f}",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            # ---------- OUTPUTS ----------
            out.write(bev)
            writer.writerow([frame_id, min_dist if min_dist != float("inf") else -1, alert])

            if frame_id % 30 == 0:
                print(f"Frame {frame_id} | Dist: {min_dist:.2f} | Alert: {alert}")

        cap.release()
        out.release()
        csv_file.close()

        print("✅ Video generado: output.mp4")
        print("✅ Eventos guardados: events.csv")
        cap.release()
