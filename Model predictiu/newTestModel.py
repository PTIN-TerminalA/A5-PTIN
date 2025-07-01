# diagnostic_test_model.py

import json
import joblib
from newPredictiveModel import setup, DEFAULT_RSSI

# Load trained model
ia = setup("position_model.pkl")
model_bssids = set(ia.bssid_list)

# Load test sample
with open("test.json") as f:
    test_data = json.load(f)

mesura = test_data["measure"]
test_bssids = {m["bssid"] for m in mesura}

# BSSID diagnostics
common = model_bssids.intersection(test_bssids)
missing = model_bssids.difference(test_bssids)
extra = test_bssids.difference(model_bssids)

print(f"Total BSSIDs in model: {len(model_bssids)}")
print(f"Total in test sample: {len(test_bssids)}")
print(f"Common BSSIDs: {len(common)}")
print(f"Missing from test: {len(missing)}")
print(f"Unexpected in test: {len(extra)}")

# Predict coordinates
x, y = ia.triangula(mesura)
print("Expected coordinates: x = 0.2048, y = 0.0840")
print(f"Predicted coordinates: x = {x}, y = {y}")
