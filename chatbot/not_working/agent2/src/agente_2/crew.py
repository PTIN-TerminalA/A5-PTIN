from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectorySearchTool
from crewai import LLM

# Model LLM
llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434", temperature=0.3)

# Eina per buscar documents
tool = DirectorySearchTool(
    directory='knowledge/',  # Canvia-ho si tens una carpeta específica pel transport
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
class Agent2():
    """Agent2 crew - Transport Intern"""

    tasks_config = 'config/tasks.yaml'  # Apunta al mateix fitxer de tasques

    @agent
    def transport_agent(self) -> Agent:
        return Agent(
            role="Coordinador de transport autònom dins de l’aeroport",
            goal="""Gestionar la mobilitat dins l’aeroport, donant informació clara sobre la disponibilitat
                de vehicles, temps d’espera, i rutes disponibles per desplaçar-se entre terminals i portes.""",
            backstory="""Ets un expert en logística i mobilitat dins d’aeroports. Coneixes al detall el sistema
                de transport intern: vehicles autònoms, temps de recorregut, disponibilitat, horaris, i rutes més eficients.
                El teu objectiu és optimitzar l’experiència de desplaçament dels passatgers.""",
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

    @task
    def transport_task(self) -> Task:
        return Task(
            config=self.tasks_config['transport_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            }
        )
