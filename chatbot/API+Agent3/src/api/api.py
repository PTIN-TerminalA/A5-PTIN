# Deixo aquests comentaris per si serveixen per la documentació
from fastapi import FastAPI, HTTPException  # FastAPI per crear l'API i HTTPException per gestionar errors
from pydantic import BaseModel  # BaseModel de Pydantic per definir models de dades
from fastapi.responses import PlainTextResponse
from src.agent3.crew import Agent3 # Importem la classe ChatBot des de l'agentCentral.crew

# Creem una instància de l'aplicació FastAPI
app = FastAPI()

# Definim el model de dades per a la petició de l'usuari
class UserRequest(BaseModel):
    user_message: str  # Atribut que conté el missatge de l'usuari

# Definim el model de dades per a la resposta de l'agent
class AgentResponse(BaseModel):
    response_text: str  # Atribut que conté la resposta de l'agent

def get_app_description():
	return (
    	"API chatbot"
	)

@app.get("/")
async def root():
	return {"message": get_app_description()}

# Definim l'endpoint que rep la petició de l'usuari i retorna la resposta de l'agent
@app.post("/ask_agent/", response_class=PlainTextResponse, responses={200: {"content": {"text/plain": {}}}})
async def ask_agent(request: UserRequest):
    try:
        # Preparem les dades d'entrada per al chatbot
        inputs = {
            "user_message": request.user_message,
            "history": ""
            }
        # Creem una instància del chatbot i obtenim la resposta
        result = Agent3().crew().kickoff(inputs=inputs)

        return result.raw

    except Exception as e:
        # Si hi ha un error, llançem una excepció HTTP amb el missatge d'error
        raise HTTPException(detail=str(e), status_code=500)
