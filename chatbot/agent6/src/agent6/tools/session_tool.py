from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import uuid
import time

# Diccionari temporal simulant una memòria per sessió
SESSION_STORE = {}

class SessionToolInput(BaseModel):
    user_message: str = Field(..., description="Missatge de l’usuari")
    session_id: str = Field(None, description="UUID actual (si existeix)")

class SessionTool(BaseTool):
    name: str = "Session Control Tool"
    description: str = "Controla l'estat de la sessió (nova, activa, inactiva, finalitzada)."
    args_schema: Type[BaseModel] = SessionToolInput

    def _run(self, user_message: str, session_id: str = None) -> str:
        now = time.time()
        comiat_keywords = ["gràcies", "adeu", "ja no necessito res", "merci"]

        if session_id is None or session_id not in SESSION_STORE:
            new_id = str(uuid.uuid4())
            SESSION_STORE[new_id] = now
            return f'{{"sessio_activa": true, "sessio_id": "{new_id}", "motiu": "nova"}}'

        last_time = SESSION_STORE[session_id]
        if now - last_time > 300:  # 5 minuts
            del SESSION_STORE[session_id]
            return f'{{"sessio_activa": false, "sessio_id": "{session_id}", "motiu": "inactivitat"}}'

        if any(k in user_message.lower() for k in comiat_keywords):
            del SESSION_STORE[session_id]
            return f'{{"sessio_activa": false, "sessio_id": "{session_id}", "motiu": "final voluntari"}}'

        SESSION_STORE[session_id] = now
        return f'{{"sessio_activa": true, "sessio_id": "{session_id}", "motiu": "activa"}}'
