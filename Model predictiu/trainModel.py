import json
import os
import numpy as np
from typing import List, Dict
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
from math import sqrt

DEFAULT_RSSI = -100.0

def load_data(json_dir: str):
    features = []
    targets = []
    all_bssids = set()
    samples = []

    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            with open(os.path.join(json_dir, filename)) as f:
                data = json.load(f)
                if "coordinates" not in data or "measurements" not in data:
                    continue
                samples.append(data)
                all_bssids.update(m['bssid'] for m in data['measurements'])

    bssid_list = sorted(list(all_bssids))
    bssid_index = {bssid: idx for idx, bssid in enumerate(bssid_list)}

    for data in samples:
        vec = [DEFAULT_RSSI] * len(bssid_list)
        for m in data['measurements']:
            if m['bssid'] in bssid_index:
                vec[bssid_index[m['bssid']]] = m['rssi']
        features.append(vec)
        targets.append([data['coordinates']['x'], data['coordinates']['y']])

    return np.array(features), np.array(targets), bssid_list

def train_model(X: np.ndarray, y: np.ndarray):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=150, random_state=12)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)
    rmse = sqrt(mean_squared_error(y_val, y_pred))
    print(f"Validation RMSE: {rmse:.4f}")
    return model

if __name__ == "__main__":
    data_dir = "pointsPruebaA"
    X, y, bssid_list = load_data(data_dir)
    model = train_model(X, y)
    joblib.dump((model, bssid_list), "position_model_user.pkl")
    print("Model saved to position_model_user.pkl")