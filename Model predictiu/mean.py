import json
import os
import numpy as np


def compute_mean_rssi(json_dir: str) -> float:
    """
    Traverse all JSON files in the given directory, extract all RSSI values,
    and return their overall mean.
    """
    rssi_values = []

    for filename in os.listdir(json_dir):
        if filename.lower().endswith('.json'):
            filepath = os.path.join(json_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: could not read {filename}: {e}")
                continue

            measures = data.get('measure', [])
            for m in measures:
                rssi = m.get('rssi')
                if isinstance(rssi, (int, float)):
                    rssi_values.append(rssi)

    if not rssi_values:
        raise ValueError(f"No valid RSSI values found in directory '{json_dir}'")

    return float(np.mean(rssi_values))


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Compute the mean RSSI value across all JSON files in a directory"
    )
    parser.add_argument(
        'json_dir',
        help='Path to directory containing JSON measurement files'
    )
    args = parser.parse_args()

    mean_rssi = compute_mean_rssi(args.json_dir)
    print(f"Mean RSSI across all files: {mean_rssi:.4f}")


if __name__ == '__main__':
    main()