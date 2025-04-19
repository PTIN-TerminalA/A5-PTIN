import cv2
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

while True:
    ret, frame = cap.read()
    if not ret:
        print("No es pot llegir cap frame de la càmera")
        break

    # Segons COCO (la llista per entrenar YOLO), classe[0] és persona
    results = model.predict(source=frame, save=False, classes=[0], verbose=False)

    quadriculaPersona = results[0].plot()

    # Mostrar el frame
    cv2.imshow("Detecció Temps Real (Persona)", quadriculaPersona)

    # Per sortir, premem q (potser moltes vegades)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Ens alliberem
cap.release()
cv2.destroyAllWindows()
