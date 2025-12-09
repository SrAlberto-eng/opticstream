import cv2
from ultralytics import YOLO

modelo = YOLO("modelo/yolo11s.pt")

fuente = cv2.VideoCapture(0)


while fuente.isOpened():

    exito, frame = fuente.read()

    if exito:
        resultados = modelo.track(frame, conf=0.8, persist=True, tracker="modelo/botsort.yaml")

        annotated_frame = resultados[0].plot()

        cv2.imshow("Inferencia", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

fuente.release()
cv2.destroyAllWindows()   