def main(mode: str = "calibration") -> None:
    """
    Punto de entrada principal de la aplicación.

    Args:
        mode (str): Modo de ejecución:
            - "calibration": herramienta de calibración
            - "video": procesamiento de video
    """
    if mode == "calibration":
        from src.tools.calibration_tool import CalibrationTool

        CalibrationTool().run()

    elif mode == "video":
        from src.app.video_processor import VideoProcessor

        VideoProcessor("data/camiones.mp4").run()

    else:
        raise ValueError(f"Modo desconocido: {mode}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="calibration")
    parser.add_argument("--video", default="data/camiones.mp4")

    args = parser.parse_args()

    main(args.mode)
