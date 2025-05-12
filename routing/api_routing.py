from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
import subprocess
import json
import os

app = FastAPI(title="API Routing")

class RouteRequest(BaseModel):
    # coordenades en píxels
    origen: Tuple[int, int]
    desti: Tuple[int, int]
    preferencies: List[str] = []

class RouteResponse(BaseModel):
    passos: int
    ruta: List[Tuple[int, int]]
    durada_estimada: float
    avis: str

@app.post("/calcular_ruta/", response_model=RouteResponse)
def calcular_ruta_api(solicitud: RouteRequest):
    if solicitud.origen == solicitud.desti:
        raise HTTPException(status_code=400, detail="Origen i destí no poden ser iguals")

    # 1. Executar el script original de càlcul de rutes
    try:
        result = subprocess.run(
    ["python", "main.py",
     f"{solicitud.origen[0]},{solicitud.origen[1]}",
     f"{solicitud.desti[0]},{solicitud.desti[1]}"],
    check=True, capture_output=True, text=True
    )
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error executant main.py: {e.stderr}")

    # 2. Llegir el fitxer path.json
    if not os.path.exists("path.json"):
        raise HTTPException(status_code=404, detail="No s'ha trobat cap ruta generada")

    with open("path.json", "r") as f:
        ruta = json.load(f)

    # 3. Calcular durada estimada (com també fa main.py)
    temps_per_pixel = 0.4
    temps_total = round(len(ruta) * temps_per_pixel, 2)

    return RouteResponse(
        ruta=ruta,
        durada_estimada=temps_total,
        avis="Ruta calculada correctament",
        passos=len(ruta)
    )
