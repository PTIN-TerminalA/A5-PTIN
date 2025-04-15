from ultralytics import YOLO

# Carreguem el model
model = YOLO("model/yolov8n.pt")
path_image = "test_images/image.jpg" #Seleccionar imatge canviant aquesta línia

# Classe 0 = persona
classes = [0]

# Fem la detecció (només persones)
results = model.predict(source=path_image, save=False, classes=classes)

# Mostrem per consola quantes persones s'han detectat
boxes = results[0].boxes  # Bounding boxes, en aquest cas persones que ha detectat YOLO 
num_persones = len(boxes)
print(f"S'han detectat {num_persones} persona/es.")
