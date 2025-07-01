import os, csv, json, warnings
# import mysql.connector
import pymysql
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

from src.assistant.crews.api.api import api
from src.assistant.crews.service.service import service, getDatosServicios
from src.assistant.crews.flights.flights import flights, getDatosVuelos
from src.assistant.crews.central.central import central

warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv(dotenv_path=Path('./.env'))

app = FastAPI()

chat_history = []

class UserRequest(BaseModel):
    user_id: int
    user_message: str
    user_location_x: float
    user_location_y: float

class AgentResponse(BaseModel):
    response_text: str

def get_app_description():
	return (
    	"API Funcional IA"
	)

@app.get("/")
async def root():
	return {"message": get_app_description()}

@app.post("/ask_agent/", response_class=PlainTextResponse, responses={200: {"content": {"text/plain": {}}}})
async def ask_agent(request: UserRequest):
    try:
        # conn = pymysql.connect(
        #     host=os.getenv("DB_HOST"),
        #     user=os.getenv("DB_USER"),
        #     password=os.getenv("DB_PASSWORD"),
        #     database=os.getenv("DB_NAME"),
        #     cursorclass=pymysql.cursors.Cursor
        # )

        # cursor = conn.cursor()

        # query = """
        # SELECT sender, message 
        # FROM (
        #     SELECT *
        #     FROM chat_message
        #     WHERE user_id = %s
        #         AND sender IN ('user', 'bot')
        #     ORDER BY date_time DESC
        #     LIMIT 4
        # ) AS ultimos
        # ORDER BY date_time ASC;
        # """

        # cursor.execute(query, (request.user_id,))
        # resultados = cursor.fetchall()
        # hist = [{'sender': r[0], 'message': r[1]} for r in resultados]

        # chat_history = "\n".join(f"{h['sender']}: {h['message']}" for h in hist)

        inputs = {
            "user_id": request.user_id,
            "user_message": request.user_message,
            "history": chat_history,
            "user_location_x": request.user_location_x,
            "user_location_y": request.user_location_y
        }

        response = ""

        raw = central().crew().kickoff(inputs=inputs)
        
        decision = raw["classified"]
        language = raw["language"]
        inputs["language"] = language

        if decision == 'commerce':
            # service_info = getDatosServicios()
            # inputs["service_info"] = service_info
            # inputs["service_info"] = json.dumps(service_info, indent=2)
            response = service().crew().kickoff(inputs=inputs)
        elif decision == 'car':
            try:
                store_names = set()
                with open("/home/iaa/assistant/knowledge/services.csv", newline='', encoding='utf-8') as archivo_csv:
                    lector = csv.DictReader(archivo_csv)
                    for fila in lector:
                        store_names.add(fila['name'].lower())

                user_message = request.user_message.strip().lower()
                matched_store = next((store for store in store_names if store in user_message), None)

                if matched_store:
                        inputs["user_message"] = matched_store
                        response = api().crew().kickoff(inputs=inputs)
                else:
                    response_text = (
                        "Botiga no trobada. Si us plau, tria una d'aquestes opcions:\n"
                        + f"\nEscriu: {inputs['user_message']} + nom_botiga\n"
                        + "\n".join(map(lambda s: f"- {s}", sorted(store_names)))
                        
                    )
                
                return response_text

            except Exception as e:
                raise Exception(f"An error occurred while running the crew: {e}")
        elif decision == 'flights':
            flight_info = getDatosVuelos(inputs.get("user_id", 0))
            
            if isinstance(flight_info, str):
                inputs["flight_info"] = flight_info
            else:
                flight_info["is_canceled"] = "Sí" if flight_info["is_canceled"] else "No"
                flight_info["is_delayed"] = "Sí" if flight_info["is_delayed"] else "No"
                inputs["flight_info"] = "\n".join(f"{k}: {v}" for k, v in flight_info.items())
            
            response = flights().crew().kickoff(inputs=inputs)
        else:
            response = "Hi ha hagut un problema. Si us plau, provi de nou."

        # chat_history.append(f"User: {request.user_message}")
        # chat_history.append(f"Assistant: {response}")
        
        # is_encrypted = 0  # o 1 si aplica

        # query = """
        # INSERT INTO chat_message (user_id, sender, message, is_encrypted)
        # VALUES (%s, %s, %s, %s);
        # """

        # valores = (request.user_id, "user", request.user_message, is_encrypted)
        # cursor.execute(query, valores)

        # valores = (request.user_id, "bot", response.raw, is_encrypted)
        # cursor.execute(query, valores)
        # conn.commit()

        # cursor.close()
        # conn.close()

        return response.raw
    except Exception as e:
        # Si hi ha un error, llançem una excepció HTTP amb el missatge d'error
        raise HTTPException(detail=str(e), status_code=500)


@app.get("/debug/history")
async def get_history():
    # return the raw list of turns so you can inspect it
    return {"history": chat_history}