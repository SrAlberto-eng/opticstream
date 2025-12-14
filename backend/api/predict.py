import cv2
import json
from ultralytics import YOLO

modelo = YOLO("modelo/yolo11s.pt")

fuente = cv2.VideoCapture(0)


while fuente.isOpened():

    exito, frame = fuente.read()

    if exito:
        resultados = modelo.track(frame, conf=0.8, persist=True, tracker="modelo/botsort.yaml")

        annotated_frame = resultados[0].plot()

        cv2.imshow("Inferencia", annotated_frame)

        predictions_list = []

        for r in resultados:
            boxes = r.boxes
            for box in boxes:
                track_id = int(box.id[0]) if box.id is not None else None
                prediction = {
                    "track_id": track_id,
                    "class_id": int(box.cls),
                    "class_name": r.names[int(box.cls)],
                    "confidence": float(box.conf)
                }
                predictions_list.append(prediction)

        with open("modelo/temp/predictions.json", "w") as f:
            json.dump(predictions_list, f, indent=4)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

fuente.release()
cv2.destroyAllWindows()   