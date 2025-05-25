import cv2
import os
import time
import json
from ultralytics import YOLO

# Carreguem el model YOLOv8
pathModel = "model/yolov8n.pt"
model = YOLO(pathModel)

# Obrim la càmera (0 = càmera default)
# En cas que amb el RockPort4 sigui diferent, hauríem de veure el número (ls /dev/video*)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No es pot accedir a la càmera.")
    exit()

print("Prem 'q' per sortir, si us plau.")


frame_count = 0
total_time = 0
detection_log = []
while True:
    ret, frame = cap.read()
    if not ret:
        print("No es pot llegir cap frame de la càmera")
        break

    #Inici mesura temps
    start = time.time()
    # Segons COCO (la llista per entrenar YOLO), classe[0] és persona
    results = model.predict(source=frame, save=False, classes=[0], verbose=False)

    # Final mesura temps
    end = time.time()

    # Calcula mètriques
    elapsed = end - start
    total_time += elapsed
    frame_count += 1
    fps = frame_count / total_time

    quadriculaPersona = results[0].plot()

    cv2.putText(quadriculaPersona,f"FPS: {fps:.2f}", (20,30), cv2.FONT_HERSHEY_SIMPLEX,0.8, (0,255,0),2)
    # Mostrar el frame
    cv2.imshow("Detecció Temps Real (Persona)", quadriculaPersona)

    #-------- Format de sortida --------
    output = {
        "frame": frame_count,
        "detections": [],
        "fps": round(fps, 2),
        "elapsed_time": round(elapsed, 4)
    }

    for i, box in enumerate(results[0].boxes):
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        confidence = float(box.conf[0])
        output["detections"].append({
            "id": i,
            "bbox": [x1, y1, x2, y2],
            "confidence": round(confidence, 4)
        })
    detection_log.append(output)
    print(json.dumps(output, indent=2))  # Mostra el format estructurat

    # Per sortir, premem q (potser moltes vegades)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

boxes = results[0].boxes
num_persones = len(boxes)
#Guardem totes les deteccions a un fitxer JSON
with open("deteccions.json","w") as f:
    json.dump(detection_log,f,indent=2)
print(f"S'han detectat {num_persones} persona/es al primer fotograma.")
print(f"Mitjana de FPS: {fps:.2f}")
print(f"Temps mitjà per fotograma: {total_time / frame_count:.4f} segons")
# Ens alliberem
cap.release()
cv2.destroyAllWindows()





