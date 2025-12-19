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
from database.repository import crear_stream, cerrar_stream, guardar_deteccion

detector = DetectorCambios()

modelo = YOLO(os.path.join(MODELO_DIR, "yolo11s.pt"))
TRACKER_PATH = os.path.join(MODELO_DIR, "botsort.yaml")
TEMP_JSON_PATH = os.path.join(MODELO_DIR, "temp", "predictions.json")

fuente = cv2.VideoCapture(0)

# Crear sesión de detección en la BD
stream_id = crear_stream("Webcam", "0")
if stream_id:
    print(f"Stream iniciado con ID: {stream_id}")
else:
    print("Error: No se pudo crear el stream en la BD")

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
                        "bbox_x": bbox[0],
                        "bbox_y": bbox[1],
                        "bbox_w": bbox[2],
                        "bbox_h": bbox[3]
                    }
                    predictions_list.append(prediction)

            hay_cambio, evento = detector.detectar_cambios(predictions_list)

            if hay_cambio and stream_id:
                if evento['nuevos_ids']:
                    tipo_evento = "entrada"
                elif evento['ids_salieron']:
                    tipo_evento = "salida"
                else:
                    tipo_evento = "cambio"
                
                deteccion_id = guardar_deteccion(
                    stream_id=stream_id,
                    total_objetos=evento['total_objetos'],
                    tipo_evento=tipo_evento,
                    predicciones=evento['predicciones']
                )
                
                if deteccion_id:
                    print(f"Guardado en BD (ID: {deteccion_id}): {evento['total_objetos']} objetos, tipo: {tipo_evento}")
                
                # DEBUG USE ONLY
                with open(TEMP_JSON_PATH, "w") as f:
                    json.dump(evento, f, indent=4, default=str)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

if stream_id:
    cerrar_stream(stream_id)
    print(f"Stream {stream_id} cerrado")

fuente.release()
cv2.destroyAllWindows()   