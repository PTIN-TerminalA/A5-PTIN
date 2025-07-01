import requests
# import mysql.connector
import pymysql
import os, csv, warnings, re
'''
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=SyntaxWarning, message=r".*\\&.*")
'''
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Optional
from pathlib import Path
from crewai.tools import tool

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

@tool("API call tool")
def my_api_call_tool(user_message: str, user_location_x: str, user_location_y: str) -> str:
    """
    This tool is used to make an API call using the given location and message.

    :param user_message: str, the destination (end_location)
    :param user_location_x: str, x coordinate
    :param user_location_y: str, y coordinate
    
    :return: str, response from the API
    """
    try:
       # Separar y convertir los valores
       #x_str, y_str, end_location = input_text.split(",")
       data = {
           "location": {
               "x": float(user_location_x.strip()),
               "y": float(user_location_y.strip())
           },
           "end_location": user_message.strip()
        }

       # Llamada POST a la API
       response = requests.post(
           "http://localhost:8000/api/reserves/app-basic",
           json=data,
           timeout=5
       )
       response.raise_for_status()
       return response.text  # O .json() si quieres el dict
    except Exception as e:
        return f"Error calling API: {e}"

@CrewBase
class api:
    """API Agent"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def api(self) -> Agent:
        return Agent(
            config=self.agents_config["api"],
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
            tools=[my_api_call_tool],
            embedder=EMBEDDER_CONFIG,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def get_api_data_task(self) -> Task:
        return Task(
            config=self.tasks_config["get_api_data_task"],
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
