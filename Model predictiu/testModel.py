import json
from predictiveModel import setup
from mapa_coord import marcar_punto_normalizado

# Load trained model
ia = setup("position_model.pkl")

# Load test sample
# És el primer fitxer de la carpeta points
with open("test.json") as f:
    test_data = json.load(f)

mesura = test_data["measure"]

# Predict coordinates
x, y = ia.triangula(mesura)

print("Expected coordinates: x= 0.4379, y =  0.2564")
print(f"Predicted coordinates: x = {x:.4f}, y = {y:.4f}")

marcar_punto_normalizado("MapaTerminalA.png", x, y) 

