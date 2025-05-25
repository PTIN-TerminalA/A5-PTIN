CameraDetection - Detecció de persones en temps real amb YOLOv8
---------------------------------------------------------------

Aquest script detecta persones en temps real a través de la webcam fent servir el model YOLOv8 preentrenat.

REQUISITS

Cal tenir instal·lades les següents llibreries: 
- ultralytics
- opencv

S'instal·len amb les següents comandes: 
pip install ultralytics 
pip install opencv-python


És recomanable fer servir un entorn virtual:

0. si no tens el paquet de creació de entorns instal·lat: 
    sudo apt install python3.12-venv
1. Navegar al directori dessitjat
2. Al directori, crea l'entorn virtual: 
    python3 -m venv venv  # crea l'entorn virtual amb el nom venv
3. Activa l'entorn virtual creat (amb nom venv): 
    source venv/bin/activate
4. Un cop fet l'entorn ja pots instal·lar les llibreries

!! Recorda que cada cop que tornis a obrir el terminal i vulguis fer servir el projecte, caldrà que reactivis l'entorn virtual amb:
	source venv/bin/activate

EXECUCIÓ:

1. Assegura’t que tens el fitxer del model YOLOv8 (yolov8n.pt) ubicat a model/yolov8n.pt.
2. Connecta una webcam al teu ordinador (la majoria d’ordinadors portàtils ja en tenen una integrada).
3. Assegura't que l'entorn virtual està activat.
4. Executa el script: python CameraDetection.py

Quan el programa comenci:
- Veuràs la imatge de la teva càmera amb una detecció (quadrat) a les persones.
- Per sortir, prem la tecla q

PER A FER SERVIR AMB UN ALTRE DISPOSITIU: 

Actualment està fet per a que detecti la càmera predeterminada que és la del portàtil (= 0), a la línia 10 del codi: 

	cap = cv2.VideoCapture(0)

Per a saber quin és el número de la càmera que es vol fer servir es consulta amb la següent comanda: 
	ls /dev/video*

El número resultant es canvia a on ara és el 0, a la línia 10 del codi: 
	cap = cv2.VideoCapture(nou_numero)
