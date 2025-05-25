import joblib
from typing import List, Dict, Tuple

DEFAULT_RSSI = -100.0

class RSSILocalizer:
    def __init__(self, model, bssid_list: List[str]):
        self.model = model
        self.bssid_list = bssid_list
        self.bssid_index = {bssid: idx for idx, bssid in enumerate(bssid_list)}

    def triangulate(self, measures: List[Dict[str, float]]) -> Tuple[float, float]:
        vec = [DEFAULT_RSSI] * len(self.bssid_list)
        for m in measures:
            bssid = m["bssid"]
            rssi = m["rssi"]
            if bssid in self.bssid_index:
                vec[self.bssid_index[bssid]] = rssi
        pred = self.model.predict([vec])[0]
        return float(pred[0]), float(pred[1])

def setup(model_path: str = "location_predictor.pkl") -> RSSILocalizer:
    model, bssid_list = joblib.load(model_path)
    return RSSILocalizer(model, bssid_list)
