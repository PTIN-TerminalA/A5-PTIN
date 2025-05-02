import cv2
#import time
from ultralytics import YOLO

# Rutes
path_model = "model/yolov8n.pt"
path_video = "test_videos/video1.mp4" # Canviar aquesta línia per a seleccionar un altre vídeo

# Carregar el model YOLOv8n preentrenat
model = YOLO(path_model)

# Obrir l'arxiu de vídeo
cap = cv2.VideoCapture(path_video)

# Verificar si el vídeo s'ha obert' correctament
if not cap.isOpened():
    print("Error: Could not open the video.")
    exit()

#frame_count = 0
#total_time = 0
# Processar el vídeo fotograma a fotograma
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Fi del video

    # Inici mesura temps
    #start = time.time()
    # Fer la detecció només per a la clase 0 (personas)
    results = model.predict(source=frame, save=False, classes=[0], verbose=False)
    # Final mesura temps
    #end = time.time()

    # Calcula mètriques
    #elapsed = end - start
    #total_time += elapsed
    #frame_count += 1
    #fps = frame_count / total_time

    # Crear el fotograma anotant els resultats
    annotated_frame = results[0].plot()
    #cv2.putText(annotated_frame,f"FPS: {fps:.2f}", (20,30), cv2.FONT_HERSHEY_SIMPLEX,0.8, (0,255,0),2)
    # Mostrar el fotograma amb anotacions
    cv2.imshow("Human Recognition Video", annotated_frame)

    # Sortir del bucle si es presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Comptem quantes persones s'han detectat
# boxes = results[0].boxes
# num_persones = len(boxes)
# print(f"S'han detectat {num_persones} persona/es al primer fotograma.")
#print(f"Mitjana de FPS: {fps:.2f}")
#print(f"Temps mitjà per fotograma: {total_time / frame_count:.4f} segons")
# Quan acaba vídeo termina
cap.release()
cv2.destroyAllWindows()
