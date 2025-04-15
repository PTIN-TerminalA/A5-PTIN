import cv2
from ultralytics import YOLO

# Rutes
path_model = "model/yolov8n.pt"
path_video = "test_videos/video1.mp4"  # Canviar aquesta línia per a seleccionar un altre vídeo

# Carregar el model YOLOv8n preentrenat
model = YOLO(path_model)

# Obrir l'arxiu de vídeo
cap = cv2.VideoCapture(path_video)

# Verificar si el vídeo s'ha obert' correctament
if not cap.isOpened():
    print("Error: Could not open the video.")
    exit()

# Processar el vídeo fotograma a fotograma
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Fi del video

    # Fer la detecció només per a la clase 0 (personas)
    results = model.predict(source=frame, save=False, classes=[0], verbose=False)

    # Crear el fotograma anotant els resultats
    annotated_frame = results[0].plot()

    # Mostrar el fotograma amb anotacions
    cv2.imshow("Human Recognition Video", annotated_frame)

    # Sortir del bucle si es presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Comptem quantes persones s'han detectat
# boxes = results[0].boxes
# num_persones = len(boxes)
# print(f"S'han detectat {num_persones} persona/es al primer fotograma.")

# Quan acaba vídeo termina
cap.release()
cv2.destroyAllWindows()
