from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import uuid
import time
from typing import Optional

# Diccionari temporal simulant una memòria per sessió
SESSION_STORE = {}

class SessionToolInput(BaseModel):
    user_message: str = Field(..., description="Missatge de l’usuari")
    session_id: Optional[str] = Field(None, description="UUID actual (si existeix)")

class SessionTool(BaseTool):
    name: str = "Session Control Tool"
    description: str = "Controla l'estat de la sessió (nova, activa, inactiva, finalitzada)."
    args_schema: Type[BaseModel] = SessionToolInput

    def _run(self, user_message: str, session_id: str = None) -> str:
        now = time.time()
        comiat_keywords = ["gràcies", "adeu", "ja no necessito res", "merci"]

        if not session_id or session_id not in SESSION_STORE:
            new_id = str(uuid.uuid4())
            SESSION_STORE[new_id] = now
            json_res = {
                "sessio_activa": True,
                "sessio_id": new_id,
                "motiu": "nova"
            }
        elif now - SESSION_STORE[session_id] > 300:
            del SESSION_STORE[session_id]
            json_res = {
                "sessio_activa": False,
                "sessio_id": session_id,
                "motiu": "inactivitat"
            }
        elif any(k in user_message.lower() for k in comiat_keywords):
            del SESSION_STORE[session_id]
            json_res = {
                "sessio_activa": False,
                "sessio_id": session_id,
                "motiu": "final voluntari"
            }
        else:
            SESSION_STORE[session_id] = now
            json_res = {
                "sessio_activa": True,
                "sessio_id": session_id,
                "motiu": "activa"
            }

        # Generem resposta de fallback per si el model no respon
        resposta_fallback = (
            f"\n\n(Session ID: {json_res['sessio_id']} | "
            f"Estat: {'activa' if json_res['sessio_activa'] else 'inactiva'} | "
            f"Motiu: {json_res['motiu']})"
        )

        import json
        return json.dumps(json_res) + resposta_fallback
