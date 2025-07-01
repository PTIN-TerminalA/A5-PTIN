#!/usr/bin/env python3
import os
import glob
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import joblib

def load_wifi_data(json_dir):
    """
    Load all JSON files in the given directory. Each JSON is expected to have:
      - 'coordinates': {'x': float, 'y': float}
      - 'measurements': list of {'bssid': str, 'rssi': int}
    Returns a pandas DataFrame with columns 'x', 'y' and one column per unique BSSID with RSSI values.
    """
    data_rows = []
    for filepath in glob.glob(os.path.join(json_dir, '*.json')):
        with open(filepath, 'r') as f:
            sample = json.load(f)

        coords = sample.get('coordinates', {})
        x = coords.get('x')
        y = coords.get('y')

        if x is None or y is None:
            continue  # skip if coordinates are missing

        row = {'x': x, 'y': y}

        measurements = sample.get('measurements', [])
        for meas in measurements:
            bssid = meas.get('bssid')
            rssi = meas.get('rssi')
            if bssid and rssi is not None:
                row[bssid] = rssi

        data_rows.append(row)

    df = pd.DataFrame(data_rows)
    return df

def preprocess_features(df):
    y = df[['x', 'y']].values.astype(np.float32)
    X = df.drop(columns=['x', 'y'])
    # Fill missing RSSI with -100 (typical min Wi-Fi RSSI)
    X_filled = X.fillna(-100)
    return X_filled.values.astype(np.float32), y

def train_and_evaluate(X, y):
    """
    Split the data into train/test, train the MultiOutput XGB model, and evaluate RMSE.
    Returns the trained model and RMSE for x and y.
    """
    # Split data (80% train, 20% test for example)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    xgb = XGBRegressor(objective='reg:squarederror', random_state=42)
    model = MultiOutputRegressor(xgb)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse_x = np.sqrt(mean_squared_error(y_test[:, 0], y_pred[:, 0]))
    rmse_y = np.sqrt(mean_squared_error(y_test[:, 1], y_pred[:, 1]))
    return model, rmse_x, rmse_y

def main():
    json_dir = "pointsPrueba"  # TODO: replace with actual path
    df = load_wifi_data(json_dir)
    if df.empty:
        raise ValueError(f"No data loaded from {json_dir}")
    X, y = preprocess_features(df)
    model, rmse_x, rmse_y = train_and_evaluate(X, y)
    print(f"Test RMSE (x): {rmse_x:.4f}, RMSE (y): {rmse_y:.4f}")
    combined_rmse = np.sqrt(rmse_x**2 + rmse_y**2)
    print(f"Combined RMSE: {combined_rmse:.4f}")
    bssid_list = df.drop(columns=["x", "y"]).columns.tolist()
    joblib.dump((model, bssid_list), 'position_model_user.pkl')
    print("Model saved to 'position_model_user.pkl'")

if __name__ == "__main__":
    main()
