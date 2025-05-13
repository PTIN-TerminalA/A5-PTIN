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

print("Expected coordinates: x= 0.43792207792207793, y =  0.2564874012786762")
print(f"Predicted coordinates: x = {x}, y = {y}")

#marcar_punto_normalizado("MapaTerminalA.png", x, y) 