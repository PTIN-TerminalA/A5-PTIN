#!/usr/bin/env python3
"""
Wi-Fi Indoor Positioning Model Trainer

This script reads JSON files containing Wi-Fi scan data and their corresponding
(x, y) coordinates, builds a machine learning model to predict positions based
on RSSI fingerprints, evaluates it, and saves the trained model.
"""

import os
import json
import glob
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import joblib

def load_data(json_dir):
    """
    Load and parse all JSON files from the directory.
    Returns: pandas DataFrame with features and target coordinates.
    """
    data = []
    for filepath in glob.glob(os.path.join(json_dir, "*.json")):
        with open(filepath, 'r') as f:
            sample = json.load(f)

        coord = sample.get("coordinates", {})
        x = coord.get("x")
        y = coord.get("y")

        if x is None or y is None:
            continue  # skip invalid entries

        row = {"x": x, "y": y}
        for ap in sample.get("measurements", []):
            bssid = ap.get("bssid")
            rssi = ap.get("rssi")
            if bssid and rssi is not None:
                row[bssid] = rssi

        data.append(row)

    df = pd.DataFrame(data)
    return df

def preprocess(df):
    """
    Prepare features and targets.
    Missing BSSID values are filled with a default RSSI of -100.
    Returns: X (features), y (targets)
    """
    y = df[["x", "y"]].values.astype(np.float32)
    X = df.drop(columns=["x", "y"]).fillna(-100).astype(np.float32)
    return X, y

def train_model(X, y):
    """
    Split data, train model, and evaluate performance.
    Returns: trained model, (rmse_x, rmse_y, combined_rmse)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = MultiOutputRegressor(XGBRegressor(
        objective="reg:squarederror",
        n_estimators=200,
        learning_rate=0.1,
        max_depth=10,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    ))

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    rmse_x = np.sqrt(mean_squared_error(y_test[:, 0], y_pred[:, 0]))
    rmse_y = np.sqrt(mean_squared_error(y_test[:, 1], y_pred[:, 1]))
    combined_rmse = np.sqrt(rmse_x**2 + rmse_y**2)

    return model, rmse_x, rmse_y, combined_rmse

def main():
    json_dir = "pointsPruebaA"  # Replace with actual path

    print("Loading data...")
    df = load_data(json_dir)
    if df.empty:
        print("No valid data found.")
        return

    print(f"Loaded {len(df)} samples, {len(df.columns)-2} unique BSSIDs.")
    X, y = preprocess(df)

    print("Training model...")
    model, rmse_x, rmse_y, combined_rmse = train_model(X, y)

    print(f"RMSE X: {rmse_x:.5f}")
    print(f"RMSE Y: {rmse_y:.5f}")
    print(f"Combined RMSE: {combined_rmse:.5f}")

    # Check if we meet the 0.05 RMSE requirement
    if combined_rmse < 0.05:
        print("✅ Target accuracy achieved!")

    print("Saving model to 'position_model.pkl'...")
    bssid_list = list(df.drop(columns=["x", "y"]).columns)
    joblib.dump((model, bssid_list), "position_model.pkl")
    print("Done.")

if __name__ == "__main__":
    main()
