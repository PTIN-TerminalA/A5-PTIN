from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from crewai import LLM


# ------------------------------
# CONFIGURACIÓ GLOBAL
# ------------------------------
EMBEDDER_CONFIG = {
    "provider": "ollama",
    "config": {
        "model": "mxbai-embed-large",
        "ollama_base_url": "http://localhost:11434"
    }
}

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "agent2_transport",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 768
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.1:latest",
            "temperature": 0,
            "max_tokens": 2000,
            "ollama_base_url": "http://localhost:11434"
        },
    },
    "embedder": EMBEDDER_CONFIG
}

llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0.2,
    config={
        "max_tokens": 150,
        "top_k": 5
    }
)

# ------------------------------
# CONEIXEMENT: Fitxers CSV
# ------------------------------

csv_source = CSVKnowledgeSource(
    file_paths=[
        'rutes_transport.csv',
        'estacions.csv'
    ],
    chunk_size=300,
    chunk_overlap=20
)

# ------------------------------
# AGENT I TASCA
# ------------------------------

@CrewBase
class AgentTransport():
    """Agent2 crew - Transport Intern"""

    @agent
    def transport_agent(self) -> Agent:
        return Agent(
            role="Agent de Transport Intern de l'Aeroport",
            goal="""Proporcionar informació precisa i actual sobre desplaçaments dins de l’aeroport, temps estimats i disponibilitat de vehicles autònoms.""",
            backstory="""Ets un assistent especialitzat en mobilitat interna d’aeroports.
            Coneixes totes les rutes, connexions i estacions. Pots assessorar els usuaris sobre la millor manera de moure’s entre terminals, portes, i serveis.
            Sempre busques oferir rutes eficients, informant amb claredat i empatia.""",
            llm=llm,
            memory=False,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": "gerard", "local_mem0_config": config},
            },
            allow_delegation=False,
            max_iter=1,
            embedder=EMBEDDER_CONFIG
        )

    @task
    def transport_task(self) -> Task:
        return Task(
            description="""
            Si l’usuari només proporciona una ubicació (per exemple: "Hi ha vehicles a la Terminal A4?"), 
            NO detectis cap origen ni destinació. NO parlis de temps, rutes, ni recomanacions. 

            Limita't a consultar `estacions.csv`. Indica el nombre de vehicles i si l’estació està activa.

            Només si hi ha clarament un origen i un destí (dues ubicacions), consulta `rutes_transport.csv` i `alternatives_transport.csv` per suggerir la millor opció.

            Historial: {history}
            Consulta: {user_message}
            """,
            expected_output="""Resposta clara i estructurada amb:
            - Punt d’origen i destinació detectats
            - Temps estimat a peu i amb vehicle
            - Disponibilitat de vehicle autònom
            - Ruta recomanada
            - Alternativa si no hi ha vehicle disponible""",
            agent=self.transport_agent()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            max_rpm=20,
            knowledge_sources=[csv_source],
            embedder=EMBEDDER_CONFIG
        )
Agent2 = AgentTransport