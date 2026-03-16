# Archivo: src/main.py
import cv2
import time

def process_video(video_path: str) -> None:
    """Abre un stream de video y muestra los FPS en tiempo real."""
    cap = cv2.VideoCapture(video_path)
    
    # Por qué el assert: VideoCapture devuelve objeto válido incluso si
    # el archivo no existe. Sin este assert, el error aparece 3 líneas
    # después con un mensaje confuso.
    assert cap.isOpened(), f"Error: No se pudo abrir {video_path}"

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        
        # FPS = 1 frame / tiempo que tardó ese frame en procesarse
        # Si tardó 0.033s → 1/0.033 = 30 FPS
        # El max(... , 1e-9) evita división por cero en el primer frame
        fps = 1.0 / max(current_time - prev_time, 1e-9)
        prev_time = current_time

        # cv2.putText(imagen, texto, posicion, fuente, escala, color_BGR, grosor)
        # Ojo: OpenCV usa BGR no RGB. Verde = (0, 255, 0)
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2
        )

        cv2.imshow("Monitor de Patio - MVP1", frame)

        # waitKey(1): da 1ms al backend GUI para renderizar el frame.
        # Sin esto la ventana no se actualiza.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video("data/camiones.mp4")