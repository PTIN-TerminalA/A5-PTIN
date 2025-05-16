import uvicorn
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
    
    wayPoints: List[Tuple[float, float]] = []
    prevDir: Tuple[int, int] = (0, 0)
    '''
    simplifiedPath: List[Tuple[float, float]] = []
    prevPath: Tuple[float, float] = (None, None)

    for x, y in path:
        pt = (round(y / maxY, 4), round((1 - (x / maxX)), 4))

        if pt != prevPath:
            simplifiedPath.append(pt)
            prevPath = pt
    '''
    for i in range(len(path)):
        x, y = path[i]

        if not (i == 0 or i == len(path) - 1):
            px, py = path[i - 1]
            dx, dy = x - px, y - py

            if (dx, dy) == prevDir:
                continue

            prevDir = (dx, dy)

        wayPoints.append((round(y / maxY, 4), round(1 - (x / maxX), 4)))
    


    return {"length": len(wayPoints), "path": wayPoints}
    #return {"length": len(simplifiedPath), "path": simplifiedPath}

if __name__ == "__main__":
    uvicorn.run("api:app", host="localhost", port=5000, reload=True)
