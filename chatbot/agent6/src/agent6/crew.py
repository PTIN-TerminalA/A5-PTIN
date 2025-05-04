from crewai import Crew, Agent, Task, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from agent6.tools.session_tool import SessionTool 

llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0.3
)

@CrewBase
class Agent6:
    tasks_config = "config/tasks.yaml"  # O la ruta correcta del teu fitxer

    @agent
    def agent_control_sessio(self) -> Agent:
        return Agent(
            role="Agent de Control de Sessió",
            goal="Controlar sessió per usuari amb UUID, timeout i finalització.",
            backstory="Monitoritzo les sessions i les tanco si cal.",
            llm=llm,
            tools=[SessionTool()],
            allow_delegation=False
        )

    @task
    def control_sessio_task(self) -> Task:
        return Task(config=self.tasks_config['control_sessio_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
