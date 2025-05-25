import cv2
import os
import time
import json
from ultralytics import YOLO

# Lista de nombres de clases COCO (80 clases)
CLASS_NAMES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote",
    "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

# Cargamos el modelo YOLOv8
pathModel = "model/yolov8n.pt"
model = YOLO(pathModel)

# Abrimos la cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se puede acceder a la cámara.")
    exit()

print("Presione 'q' para salir")

frame_count = 0
total_time = 0
detection_log = []

# Lista (set) para guardar objetos detectados únicos
objetos_detectados = set()

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se puede leer el frame de la cámara")
        break

    start = time.time()
    results = model.predict(source=frame, save=False, verbose=False)
    end = time.time()

    elapsed = end - start
    total_time += elapsed
    frame_count += 1
    fps = frame_count / total_time

    annotated_frame = results[0].plot()
    cv2.putText(annotated_frame, 
                f"FPS: {fps:.2f}", 
                (20,30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, 
                (0,255,0), 
                2)
    
    cv2.imshow("Detección de Objetos en Tiempo Real", annotated_frame)

    output = {
        "frame": frame_count,
        "detections": [],
        "fps": round(fps, 2),
        "elapsed_time": round(elapsed, 4)
    }

    for i, box in enumerate(results[0].boxes):
        cls_id = int(box.cls[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        confidence = float(box.conf[0])
        class_name = CLASS_NAMES[cls_id]

        # Añadir clase al conjunto de objetos detectados
        objetos_detectados.add(class_name)

        output["detections"].append({
            "id": i,
            "class_id": cls_id,
            "class_name": class_name,
            "bbox": [x1, y1, x2, y2],
            "confidence": round(confidence, 4)
        })
    
    detection_log.append(output)
    print(json.dumps(output, indent=2))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Guardar resultados
with open("detecciones.json", "w") as f:
    json.dump(detection_log, f, indent=2)

# Estadísticas finales
if detection_log:
    primer_frame_detections = detection_log[0]["detections"]
    print(f"\nResumen final:")
    print(f"Total de frames procesados: {frame_count}")
    print(f"En el primer frame se detectaron: {len(primer_frame_detections)} objetos")
    print(f"Clases detectadas en primer frame: {list(set(d['class_name'] for d in primer_frame_detections))}")

# Imprimir todos los objetos únicos detectados
print(f"\nObjetos detectados únicos durante la sesión:")
print(sorted(list(objetos_detectados)))

# Rendimiento promedio
#print(f"\nRendimiento promedio:")
#print(f"FPS promedio: {fps:.2f}")
#print(f"Tiempo promedio por frame: {total_time / frame_count:.4f} segundos")

cap.release()
cv2.destroyAllWindows()
