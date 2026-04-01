import cv2
import time
import cProfile
import pstats
import numpy as np

from src.core.mapper import HomographyMapper, Point2D
from src.detection.hsv_tracker import get_centroids


def process_video_headless(video_path: str, mapper: HomographyMapper, num_frames: int = 100):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: No se pudo abrir {video_path}")
        return

    frames_processed = 0
    start_time = time.time()

    while frames_processed < num_frames:
        ret, frame = cap.read()
        if not ret:
            break

        # 1. BEV
        bev = mapper.transform_frame(frame, (500, 500))

        # 2. HSV
        hsv = cv2.cvtColor(bev, cv2.COLOR_BGR2HSV)

        # 3. mask
        lower_color = np.array([20, 100, 100])
        upper_color = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # 4. centroids
        centroids = get_centroids(mask)

        frames_processed += 1

    end_time = time.time()
    cap.release()

    total_time = end_time - start_time
    fps = frames_processed / max(total_time, 1e-9)

    print(f"\n--- Benchmark Results for {video_path} ---")
    print(f"Frames processed: {frames_processed}")
    print(f"Total time: {total_time:.4f} seconds")
    print(f"Average FPS: {fps:.2f}\n")


def run_profiler(video_path: str):
    mapper = HomographyMapper()

    src = [
        Point2D(100, 100),
        Point2D(500, 100),
        Point2D(500, 400),
        Point2D(100, 400),
    ]

    dst = [
        Point2D(0, 0),
        Point2D(500, 0),
        Point2D(500, 500),
        Point2D(0, 500),
    ]

    mapper.calibrate(src, dst)

    profiler = cProfile.Profile()
    profiler.enable()

    process_video_headless(video_path, mapper, num_frames=200)

    profiler.disable()

    print("\n--- Top 10 most expensive functions ---")
    stats = pstats.Stats(profiler)
    stats.sort_stats("cumtime").print_stats(10)


if __name__ == "__main__":
    test_video = "data/trucks.mp4"
    run_profiler(test_video)