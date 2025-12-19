import cv2
import json
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(SCRIPT_DIR)
MODELO_DIR = os.path.join(BACKEND_DIR, "modelo")

sys.path.append(BACKEND_DIR)

from ultralytics import YOLO
from services.detector import DetectorCambios

detector = DetectorCambios()

modelo = YOLO(os.path.join(MODELO_DIR, "yolo11s.pt"))
TRACKER_PATH = os.path.join(MODELO_DIR, "botsort.yaml")
TEMP_JSON_PATH = os.path.join(MODELO_DIR, "temp", "predictions.json")

fuente = cv2.VideoCapture(0)

contador_frames = 0
PROCESAR_CADA = 5 

while fuente.isOpened():

    exito, frame = fuente.read()

    if exito:

        contador_frames += 1

        if contador_frames % PROCESAR_CADA == 0:
            resultados = modelo.track(frame, conf=0.5, persist=True, classes=[0, 2, 3, 5, 7, 15, 16], tracker=TRACKER_PATH)

            annotated_frame = resultados[0].plot()

            cv2.imshow("Inferencia", annotated_frame)

            predictions_list = []

            for r in resultados:
                boxes = r.boxes
                for box in boxes:
                    track_id = int(box.id[0]) if box.id is not None else None
                    bbox = box.xywh[0].tolist()
                    prediction = {
                        "track_id": track_id,
                        "class_id": int(box.cls),
                        "class_name": r.names[int(box.cls)],
                        "confidence": float(box.conf),
                    }
                    predictions_list.append(prediction)

            hay_cambio, evento = detector.detectar_cambios(predictions_list)

            if hay_cambio:
                with open(TEMP_JSON_PATH, "w") as f:
                    json.dump(evento, f, indent=4)
                print(f"Cambio detectado: {evento['total_objetos']} objetos, nuevos: {evento['nuevos_ids']}, salieron: {evento['ids_salieron']}")

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

fuente.release()
cv2.destroyAllWindows()   