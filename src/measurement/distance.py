import math
import cv2
import numpy as np
import os

def pixels_to_meters(px_distance, scale_factor):
    """Convierte distancia en píxeles a metros."""
    return px_distance * scale_factor


def test_pixels_to_meters():
    # Test de validación numérica: si 100px son 2.5 metros, scale_factor = 2.5/100 = 0.025
    dist = pixels_to_meters(100, 0.025)
    # ??? Agrega un assert usando math.isclose para validar que dist es 2.5
    assert math.isclose(dist, 2.5), f"Error numérico: {dist} != 2.5"
    print("Test unitario pixels_to_meters: VERDE")


# Estado global para medir
measurement_points = []
# Factor simulado: asume que calibramos y 1 píxel BEV = 0.05 metros
SCALE_FACTOR = 0.05


def measure_callback(event, x, y, flags, param):
    global measurement_points
    if event == cv2.EVENT_LBUTTONDOWN:
        measurement_points.append((x, y))
        # ??? Lógica FIFO de 2 puntos: si len > 2, conserva solo el clic actual
        if len(measurement_points) > 2:
            measurement_points = [(x, y)]


def main():
    test_pixels_to_meters()

    # Frame simulando la salida BEV del Día 6
    bev_frame = np.zeros((600, 600, 3), dtype=np.uint8)
    cv2.putText(bev_frame, "Haz clic en 2 puntos para medir. 'q' para salir.", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    
    cv2.namedWindow("Medicion BEV")
    # ??? Configura el callback del mouse para la ventana "Medicion BEV"
    cv2.setMouseCallback("Medicion BEV", measure_callback)
    
    while True:
        display = bev_frame.copy()
        
        # Renderizar clics
        for pt in measurement_points:
            cv2.circle(display, pt, 5, (0, 0, 255), -1)

        if len(measurement_points) == 2:
                p1, p2 = measurement_points[0], measurement_points[1]
                
                # ??? Dibuja una línea entre p1 y p2 (usa cv2.line)
                cv2.line(display, p1, p2, (0, 255, 0), 2)
                
                # ??? Calcula la distancia euclidiana en píxeles (usa math.hypot)
                px_dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
                
                # ??? Llama a tu función pixels_to_meters
                m_dist = pixels_to_meters(px_dist, SCALE_FACTOR)
                
                # Dibujar el texto de medición en el punto medio
                mid_point = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
                cv2.putText(display, f"{m_dist:.2f} m", mid_point, 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        cv2.imshow("Medicion BEV", display)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                
    cv2.destroyAllWindows()


if __name__ == "__main__":
    os.makedirs("src/measurement", exist_ok=True)
    main()  