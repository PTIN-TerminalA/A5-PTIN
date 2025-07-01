# Deixo aquests comentaris per si serveixen per la documentació
from typing import List, Optional
from fastapi import FastAPI, HTTPException  # FastAPI per crear l'API i HTTPException per gestionar errors
from pydantic import BaseModel  # BaseModel de Pydantic per definir models de dades
from fastapi.responses import PlainTextResponse
from src.agent3.crew import Agent3 # Importem la classe ChatBot des de l'agentCentral.crew
from dotenv import load_dotenv
import os
from pathlib import Path
import mysql.connector
from mem0 import MemoryClient


dotenv_path = Path('./src/agent3/') / '.env'
load_dotenv(dotenv_path=dotenv_path)
# Creem una instància de l'aplicació FastAPI
app = FastAPI()

history = []

# Definim el model de dades per a la petició de l'usuari
class UserRequest(BaseModel):
    user_id: int #atribut que conté id usuari 
    user_message: str  # Atribut que conté el missatge de l'usuari
    #history: Optional[List[str]] = []

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

        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        cursor = conn.cursor()

        query = """
        SELECT sender, message 
        FROM (
            SELECT *
            FROM chat_message
            WHERE user_id = %s
                AND sender IN ('user', 'bot')
            ORDER BY date_time DESC
            LIMIT 6
        ) AS ultimos
        ORDER BY date_time ASC;
        """

        cursor.execute(query, (request.user_id,))
        resultados = cursor.fetchall()
        hist = [{'sender': r[0], 'message': r[1]} for r in resultados]

        chat_history = "\n".join(f"{h['sender']}: {h['message']}" for h in hist)
        #hist = resultados or []
        #chat_history = "\n".join(hist[-2:]) if len(hist) >= 2 else ""

        inputs = {
            "user_id": request.user_id,
            "user_message": request.user_message,
            "history": chat_history
        }
        # Creem una instància del chatbot i obtenim la resposta
        result = Agent3().crew().kickoff(inputs=inputs)

        history.append(f"User: {request.user_message}")
        history.append(f"Assistant: {result}")
        

        is_encrypted = 0  # o 1 si aplica

        query = """
        INSERT INTO chat_message (user_id, sender, message, is_encrypted)
        VALUES (%s, %s, %s, %s);
        """

        valores = (request.user_id, "user", request.user_message, is_encrypted)
        cursor.execute(query, valores)

        valores = (request.user_id, "bot", result.raw, is_encrypted)
        cursor.execute(query, valores)
        conn.commit()

        cursor.close()
        conn.close()

        return result.raw
    except Exception as e:
        # Si hi ha un error, llançem una excepció HTTP amb el missatge d'error
        raise HTTPException(detail=str(e), status_code=500)


@app.get("/debug/history")
async def get_history():
    # return the raw list of turns so you can inspect it
    return {"history": history}