import json
from predictiveModel import setup

# Load trained model
ia = setup("position_model_user.pkl")

# Load test sample
# És el primer fitxer de la carpeta points
with open("test.json") as f:
    test_data = json.load(f)

mesura = test_data["measure"]

# Predict coordinates
x, y = ia.triangula(mesura)

print("Expected coordinates: x = 0.4607, y = 0.8439")
print(f"Predicted coordinates: x = {x}, y = {y}")

with open("testA.json") as fA:
    test_dataA = json.load(fA)

mesuraA = test_dataA["measure"]

# Predict coordinates
xA, yA = ia.triangula(mesuraA)

print("Expected coordinates: x = 0.3665, y = 0.0666")
print(f"Predicted coordinates: x = {xA}, y = {yA}")
