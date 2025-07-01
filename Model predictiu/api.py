from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Tuple
from predictiveModel import setup

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
    global localizerCar, localizerUser

    try:
        localizerCar = setup("position_model_car.pkl")
        localizerUser = setup("position_model_user.pkl")
    except Exception as e:
        raise RunTimeException(e)

@app.post("/localizeCar", response_model=Position)
def localize(conjunt: MeasurementGroup):

    if localizerCar is None:
        raise HTTPException(status_code=500, detail="El model del cotxe no està carregat!")

    data = [m.dict() for m in conjunt.measure]

    try:
        x, y = localizerCar.triangula(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return Position(x=x, y=y)

@app.post("/localizeUser", response_model=Position)
def localize(conjunt: MeasurementGroup):

    if localizerUser is None:
        raise HTTPException(status_code=500, detail="El model del usuari no està carregat!")

    data = [m.dict() for m in conjunt.measure]

    try:
        x, y = localizerUser.triangula(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return Position(x=x, y=y)

