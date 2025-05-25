from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Tuple, List

from datastructure import imageToMatrix
from pathfinding import AStar

gridMap = imageToMatrix("TerminalA.jpg")

app = FastAPI()

class PointRequest(BaseModel):
    start: Tuple[float, float]
    goal: Tuple[float, float]

def normalizeCoord(xNorm: float, yNorm: float, height: int, width: int) -> Tuple[int, int]:
    j = int(round((width - 1) * xNorm))
    i = int(round((height - 1) * (1 - yNorm)))
    return (i, j) 

@app.get("/")
def readRoot():
    return {"message": "Estat de l'API de Routing: Funcional."}

@app.post("/path")
def getPath(data: PointRequest):
    pathfinder = AStar(gridMap)

    xStart, yStart = data.start
    xGoal, yGoal = data.goal

    start = normalizeCoord(xStart, yStart, gridMap.height, gridMap.width)
    goal = normalizeCoord(xGoal, yGoal, gridMap.height, gridMap.width)

    if not gridMap.isFree(*start):
        raise HTTPException(status_code=400, detail=f"El punt start: {start} està ocupat per un obstacle.")
    if not gridMap.isFree(*goal):
        raise HTTPException(status_code=400, detail=f"El punt goal: {goal} està ocupat per un obstacle.")

    path = pathfinder.findPath(start, goal)

    if not path:
        raise HTTPException(status_code=404, detail="No path found")

    maxX = max(gridMap.height - 1, 1)
    maxY = max(gridMap.width - 1, 1)

    normalizedPath = [
        ((y / maxY), 1 - (x / maxX)) for (x, y) in path
    ]

    return {"length": len(path), "path": normalizedPath}
