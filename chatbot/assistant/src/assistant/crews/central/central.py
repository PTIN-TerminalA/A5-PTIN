import os, csv, warnings, re
'''
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=SyntaxWarning, message=r".*\\&.*")
'''
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
# from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Optional
from pathlib import Path

# dotenv_path = Path('./src/assistant/') / '.env'
# load_dotenv(dotenv_path=dotenv_path)

class CentralClassification(BaseModel):
    classified: str = Field(
        ...,
        description="The category assigned based on the user input. Must be one of: 'car', 'flights', or 'commerce'."
    ),
    language: str = Field(
        ...,
        description="The language of the user input"
    )
    

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
            "model": "gemma2:latest",
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
    model="ollama/gemma2:latest",  # Versión más ligera
    base_url="http://10.60.0.3:11434",
    temperature=0.3,
    config={
        "max_tokens": 200,  # Limita respuesta
        "top_k": 10         # Reduce opciones de sampling
    }
)

@CrewBase
class central:
    """Central Agent"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def central(self) -> Agent:
        return Agent(
            config=self.agents_config["central"],
            verbose=True,
            llm=llm,
            memory=True,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": '{user_id}', 'local_mem0_config': config},
            },
            allow_delegation=False,
            # max_retry=1,
            # max_iter=1,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def classify_input(self) -> Task:
        return Task(
            config=self.tasks_config["classify_input"],
            output_pydantic=CentralClassification,
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
