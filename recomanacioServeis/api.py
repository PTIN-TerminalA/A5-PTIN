from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from recommendation import kickoff

app = FastAPI()

class UserInfo(BaseModel):
    x: float
    y: float
    id: int

@app.post("/recommendation")
def recommend(user: UserInfo):
    
    result = kickoff(user.x, user.y, user.id)
    if result is None:
        return {"recommendation": None}
    return {"recommendation": result}
