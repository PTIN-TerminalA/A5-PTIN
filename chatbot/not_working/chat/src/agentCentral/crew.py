from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool
from crewai_tools import DirectorySearchTool
from typing import List, Optional
from dotenv import load_dotenv
from crewai import LLM
import yaml
import os

llm= LLM(model="ollama/gemma3:1b", base_url="http://localhost:11434", temperature=0.3)

tool = DirectorySearchTool(
    directory='knowledge/',
    config=dict(
        llm=dict(
            provider="ollama",
            config=dict(
                base_url="http://localhost:11434",
                model="gemma3:1b",
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
    # Load agent and task configurations from YAML files
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = os.path.join(base_dir, "config")

        agents_path = os.path.join(config_dir, "agents.yaml")
        tasks_path = os.path.join(config_dir, "tasks.yaml")

        with open(agents_path, "r") as f:
            self.agents_config = yaml.safe_load(f)

        with open(tasks_path, "r") as f:
            self.tasks_config = yaml.safe_load(f)

    # agents_config = 'config/agents.yaml'
    # tasks_config = 'config/tasks.yaml'

    @agent
    def manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['manager_agent'],
            allow_delegation=True,
            llm=llm,
            # memòria?
            memory=True,
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            }
        )

    @agent
    def qa_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_agent'],
            llm=llm,
            tools=[tool],
            allow_delegation=False,
            memory=True,
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            } 
        )

    # declarar més agents

    @task
    def answer_question_task(self) -> Task:
        return Task(
            config=self.tasks_config['answer_question_task'],
            agent=self.qa_agent()
        )

    # declarar més tasques

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.qa_agent()],
            tasks=[self.answer_question_task()],
            process=Process.hierarchical,
            manager_agent=self.manager_agent(),
            #manager_llm=?
            verbose=True, 
            memory=True,
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            }, 
        )