from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool
from crewai_tools import DirectorySearchTool

from typing import List, Optional

from dotenv import load_dotenv

from crewai import LLM




# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

llm= LLM(model="ollama/llama3.1", base_url="http://localhost:11434", temperature=0.3)

tool = DirectorySearchTool(
    directory='knowledge/',
    config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama3.1",
                #top_k=50,    
                #max_tokens=2000, 
                # temperature=0.5,
                # top_p=1,
                stream=True,
            ),
        ),
        embedder=dict(
            provider="ollama", # or openai, ollama, ...
            config=dict(
                model="mxbai-embed-large",
                # title="Embeddings",
            ),
        ),
    )
)


@CrewBase
class Agent3():
    """Agent3 crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
   # agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'


    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def qa_agent(self) -> Agent:
        return Agent(
           # config=self.agents_config['agente_servicios_comerciales'],
            role="Experto multilingüe en servicios de aeropuerto",
            goal="""Responde a preguntas específicas sobre los servicios disponibles en el aeropuerto,
                proporcionando información clara y útil basada en los datos del CSV.
                Exprésate de manera natural, amigable y conversacional, como si hablaras con una persona.
                Detecta automáticamente el idioma en que se formula la pregunta y responde en ese mismo idioma.
                Si la pregunta no se puede responder con el CSV, dilo claramente y ofrece una alternativa si es posible.""",
            backstory="""Eres un experto en servicios aeroportuarios con acceso a una base de datos
                        detallada en formato CSV. Tu objetivo es ayudar a las personas a encontrar respuestas rápidas y precisas.
                        Siempre respondes en el mismo idioma que usa la persona al preguntar (por ejemplo, español, inglés o catalán).""",
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

    # @agent
    # def reporting_analyst(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['reporting_analyst'],
    #         verbose=True
    #     )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def answer_question_task(self) -> Task:
        return Task(
            config=self.tasks_config['answer_question_task'],
        )

    # @task
    # def reporting_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['reporting_task'],
    #         output_file='report.md'
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the Agent3 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
           # knowledge_sources=[self.csv_source],
            verbose=True,
            memory=True,  # Enable memory for the crew
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            }, 
              
        )