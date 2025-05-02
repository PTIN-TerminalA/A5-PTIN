from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool
from crewai_tools import DirectorySearchTool
from typing import List, Optional
from dotenv import load_dotenv
from crewai import LLM
import yaml

llm= LLM(
    model="ollama/llama3.1", 
    base_url="http://localhost:11434", 
    temperature=0.3,
    config={
        "max_tokens": 200,
        "top_k": 10
    }
    )

# Configuració per a memòria externa (mem0)
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.1"
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text"
        },
    },
}

# Eina per buscar dins la carpeta knowledge
tool = DirectorySearchTool(
    directory='knowledge/',
    config=dict(
        llm=dict(
            provider="ollama",
            config=dict(
                model="llama3.1",
                stream=True,
            ),
        ),
        embedder=dict(
            provider="ollama",
            config=dict(
                model="mxbai-embed-large",
            ),
        ),
    )
)

@CrewBase
class ChatBot():
    def __init__(self):
        # Load agent and task configurations from YAML files
        with open('src/agentCentral/config/agents.yaml') as f:
            self.agents_config = yaml.safe_load(f)
        with open('src/agentCentral/config/tasks.yaml') as f:
            self.tasks_config = yaml.safe_load(f)

    # agents_config = 'config/agents.yaml'
    # tasks_config = 'config/tasks.yaml'

    @agent
    def manager_agent(self, user_id: str) -> Agent:
        return Agent(
            config=self.agents_config['manager_agent'],
            allow_delegation=True,
            llm=llm,
            memory=True,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": user_id, "local_mem0_config": config},
            },
            max_iter=1,
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            }
        )

    @agent
    def qa_agent(self, user_id: str) -> Agent:
        return Agent(
            config=self.agents_config['qa_agent'],
            llm=llm,
            tools=[tool],
            allow_delegation=False,
            memory=True,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": user_id, "local_mem0_config": config},
            },
            max_iter=1,
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            } 
        )

    # declarar més agents

    @task
    def answer_question_task(self, agent_instance: Agent) -> Task:
        return Task(
            config=self.tasks_config['answer_question_task'],
            #agent=self.qa_agent()
            agent=agent_instance
        )

    # declarar més tasques

    @crew
    def crew(self, inputs: dict) -> Crew:
        user_id = inputs.get("user_id", "default")  # si no hi és, posa default
        qa = self.qa_agent(user_id)
        manager = self.manager_agent(user_id)
        task = self.answer_question_task(qa)
        return Crew(
            agents=[qa],
            tasks=[task],
            process=Process.hierarchical,
            manager_agent=manager,
            #manager_llm=?
            verbose=True, 
            memory=True,
            max_rpm=20,
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            }, 
        )