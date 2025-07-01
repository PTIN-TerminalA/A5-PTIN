# import mysql.connector
import pymysql
import os, csv, warnings, re
'''
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=SyntaxWarning, message=r".*\\&.*")
'''
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Optional
from pathlib import Path

# dotenv_path = Path('./src/assistant/') / '.env'
# load_dotenv(dotenv_path=dotenv_path)

load_dotenv(dotenv_path=Path('./.env'))

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

EMBEDDER_CONFIG = {
    "provider": "ollama",
    "config": {
        "model": "nomic-embed-text"  # Usa el mismo modelo en todas partes
    }
}

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "assistant",
            "host": "10.60.0.3",
            "port": 6333,
            "embedding_model_dims": 768,  # Change this according to your local model's dimensions
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.2:latest",
            "temperature": 0,
            "max_tokens": 2000,
            "ollama_base_url": "http://10.60.0.3:11434",  # Ensure this URL is correct
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text:latest",
            "ollama_base_url": "http://10.60.0.3:11434",
        },
    },
}

llm = LLM (
    model="ollama/llama3.2:latest",  # Versión más ligera
    base_url="http://10.60.0.3:11434",
    temperature=0.3,
    config={
        "max_tokens": 200,  # Limita respuesta
        "top_k": 10         # Reduce opciones de sampling
    }
)

def getDatosVuelos(user_id: int):
    conn = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.Cursor
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
class flights:
    """Flights Agent"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def flights(self) -> Agent:
        return Agent(
            config=self.agents_config["flights"],
            verbose=True,
            llm=llm,
            memory=True,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": '{user_id}', 'local_mem0_config': config},
            },
            allow_delegation=False,
            # max_retry=1,
            max_iter=1,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def flight_info(self) -> Task:
        return Task(
            config=self.tasks_config["flight_info"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            embedder=EMBEDDER_CONFIG,
        )
