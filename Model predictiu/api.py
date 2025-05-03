from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Tuple
from predictiveModel import setup, RSSILocalizer, DEFAULT_RSSI

app = FastAPI()

class Measurement(BaseModel):
    bssid: str
    rssi: float

class Position(BaseModel):
    x: float
    y: float

class MeasurementGroup(BaseModel):
    measure: List[Measurement]

@app.on_event("startup")
def load_model():
    global localizer

    try:
        localizer = setup("position_model.pkl")
    except Exception as e:
        raise RunTimeException(e)

@app.post("/localize", response_model=Position)
def localize(conjunt: MeasurementGroup):

    if localizer is None:
        raise HTTPException(status_code=500, detail="No hi ha cap model carregat!")

    data = [m.dict() for m in conjunt.measure]

    try:
        x, y = localizer.triangula(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return Position(x=x, y=y)

