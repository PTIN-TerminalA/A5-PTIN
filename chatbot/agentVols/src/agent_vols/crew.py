from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai import LLM
from mem0 import MemoryClient

import mysql.connector
from pathlib import Path
from dotenv import load_dotenv
import os

# Carreguem variables d'entorn
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

llm = LLM(
    model="ollama/llama3.2",
    base_url="http://10.60.0.3:11434",
    temperature=0.3,
    config={"max_tokens": 200, "top_k": 10}
)

def obtenir_dades_vol(user_id: int):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    query = """
        SELECT
            f.flight_number,
            f.date,
            f.departure_time,
            f.arrival_time,
            f.boarding_time,
            f.origin_name,
            f.destination_name,
            f.is_canceled,
            f.is_delayed,
            g.gate_number,
            a.name AS airline_name,
            t.seat,
            t.class
        FROM ticket t
        JOIN flight f ON t.flight_id = f.id
        JOIN airline a ON f.airline_id = a.id
        LEFT JOIN flight_gate fg ON f.id = fg.flight_id
        LEFT JOIN gate g ON fg.gate_id = g.id
        WHERE t.user_id = %s
        ORDER BY f.date DESC, f.departure_time DESC
        LIMIT 1;
    """
    cursor.execute(query, (user_id,))
    resultat = cursor.fetchone()
    columnas = [desc[0] for desc in cursor.description]
    conn.close()
    if not resultat:
        return "No tens cap vol reservat."
    return dict(zip(columnas, resultat))


@CrewBase
class AgentVols:

    def __init__(self):
        self._agent = self.assistent_vols()
        self._task = self.task_vol_info()
        self.agents = [self._agent]
        self.tasks = [self._task]

    @agent
    def assistent_vols(self) -> Agent:
        return Agent(
            role="Asistent de vols",
            goal="Donar informació personalitzada sobre el vol de l'usuari",
            backstory="""Ets un assistent virtual connectat a la base de dades d’un aeroport. Tens accés a informació en temps real del vol del passatger: número, horari, porta, estat i més.""",
            llm=llm,
            memory=True,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": '{user_id}'},
            },
            allow_delegation=False,
            max_iter=1,
        )

    @task
    def task_vol_info(self) -> Task:
        return Task(
            description="""Aquest és l'historial de conversa: 
{history}

Aquest és el missatge actual: 
{user_message}

Això és el que saps del vol de l'usuari:
{vol_info}

Genera una resposta útil, clara i personalitzada per a l'usuari.""",
            expected_output="""Resposta completa amb:
- Número de vol
- Data i hora de sortida
- Porta d’embarcament
- Estat del vol (a temps, endarrerit, cancel·lat…)
- Companyia aèria
- Destinació
- Informació addicional si és rellevant (seient, classe, etc.)""",
            agent=self.assistent_vols()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def kickoff(self, inputs: dict):
        # Carrega automàticament les dades del vol i afegeix-les a inputs
        vol_info = obtenir_dades_vol(inputs.get("user_id", 0))
        inputs["vol_info"] = vol_info if isinstance(vol_info, str) else "\n".join(f"{k}: {v}" for k, v in vol_info.items())
        return self.crew().kickoff(inputs=inputs)
