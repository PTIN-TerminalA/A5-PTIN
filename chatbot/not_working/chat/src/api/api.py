# Deixo aquests comentaris per si serveixen per la documentació
from fastapi import FastAPI, HTTPException  # FastAPI per crear l'API i HTTPException per gestionar errors
from pydantic import BaseModel  # BaseModel de Pydantic per definir models de dades
from agentCentral.crew import ChatBot  # Importem la classe ChatBot des de l'agentCentral.crew

# Creem una instància de l'aplicació FastAPI
app = FastAPI()

# Definim el model de dades per a la petició de l'usuari
class UserRequest(BaseModel):
    user_message: str  # Atribut que conté el missatge de l'usuari

# Definim el model de dades per a la resposta de l'agent
class AgentResponse(BaseModel):
    response_text: str  # Atribut que conté la resposta de l'agent

# Definim l'endpoint que rep la petició de l'usuari i retorna la resposta de l'agent
@app.post("/ask_agent/", response_model=AgentResponse)
async def ask_agent(request: UserRequest):
    try:
        # Preparem les dades d'entrada per al chatbot
        inputs = {"user_message": request.user_message}
        # Creem una instància del chatbot i obtenim la resposta
        result = ChatBot().crew().kickoff(inputs=inputs)
        # Retornem la resposta de l'agent
        return AgentResponse(response_text=result)
    except Exception as e:
        # Si hi ha un error, llançem una excepció HTTP amb el missatge d'error
        raise HTTPException(detail=str(e), status_code=500)
