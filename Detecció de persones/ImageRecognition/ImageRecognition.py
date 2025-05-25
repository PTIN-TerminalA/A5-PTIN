import cv2
from ultralytics import YOLO

# Paths
path_model = "model/yolov8n.pt"
path_image = "test_images/image.jpg" #Seleccionar imatge canviant aquesta línia

# COCO-pretrained YOLOv8n model
model = YOLO(path_model)
result = model(path_image)

# Seleccionem qué clases processar
# Foro que mostra totes les classes del model: (https://stackoverflow.com/questions/77477793/class-ids-and-their-relevant-class-names-for-yolov8-model)
classes = [0] #Seleccionem humans (classe 0)

# Creem el resultat
results = model.predict(source=path_image, save=False, classes=classes)

# Mostrem per consola quantes persones s'han detectat
boxes = results[0].boxes  # Bounding boxes, en aquest cas persones que ha detectat YOLO 
num_persones = len(boxes)
print(f"S'han detectat {num_persones} persona/es.")

# Visualitza els resultats
annotated_frame = results[0].plot()  # Crea la imatge amb les anotacions
cv2.imshow("Human Detection", annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

"test_images/image.jpg"