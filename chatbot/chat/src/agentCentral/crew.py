from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool
from crewai_tools import DirectorySearchTool
from typing import List, Optional
from dotenv import load_dotenv
from crewai import LLM
import yaml

llm= LLM(model="ollama/llama3.1", base_url="http://localhost:11434", temperature=0.3)

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
    def manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['manager_agent'],
            allow_delegation=True,
            llm=llm,
            # memòria?
            memomry=True,
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