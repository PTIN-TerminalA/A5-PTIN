from agent3.tools.session_tool import SessionTool

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
