def main(mode: str = "calibration") -> None:
    """
    Main entry point of the application.

    Args:
        mode (str): Execution mode:
            - "calibration": calibration tool
            - "video": video processing
    """
    if mode == "calibration":
        from src.tools.calibration_tool import CalibrationTool

        CalibrationTool().run()

    elif mode == "video":
        from src.app.video_processor import VideoProcessor

        VideoProcessor("data/trucks.mp4").run()

    else:
        raise ValueError(f"Unknown mode: {mode}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="calibration")
    parser.add_argument("--video", default="data/trucks.mp4")

    args = parser.parse_args()

    main(args.mode)
