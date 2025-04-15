import cv2
from ultralytics import YOLO

# Rutes
path_model = "model/yolov8n.pt"
path_video = "test_videos/video1.mp4"

# Carregar el model
model = YOLO(path_model)

# Obrir el vídeo
cap = cv2.VideoCapture(path_video)

# Comprovar si el vídeo s’ha pogut obrir
if not cap.isOpened():
    print("Error: No s'ha pogut obrir el vídeo.")
    exit()

# Llegim només el primer fotograma
ret, frame = cap.read()
if ret:
    # Guardem el fotograma com a imatge
    cv2.imwrite("fotograma_inicial.jpg", frame)
    print("S'ha guardat el primer fotograma com a 'fotograma_inicial.jpg'.")

    # Detecció només de persones (classe 0)
    results = model.predict(source=frame, save=False, classes=[0], verbose=False)

    # Comptem quantes persones s'han detectat
    boxes = results[0].boxes
    num_persones = len(boxes)
    print(f"S'han detectat {num_persones} persona/es al primer fotograma.")

# Alliberar el vídeo
cap.release()
