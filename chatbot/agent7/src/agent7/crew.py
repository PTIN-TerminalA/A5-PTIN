from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from crewai.tools import tool
from typing import List, Optional
from crewai import LLM

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
            "collection_name": "agent7",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 768,
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.1:latest",
            "temperature": 0,
            "max_tokens": 2000,
            "ollama_base_url": "http://localhost:11434",
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text:latest",
            "ollama_base_url": "http://localhost:11434",
        },
    },
}

llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0.3,
    config={
        "max_tokens": 200,
        "top_k": 10
    }
)

csv_source = CSVKnowledgeSource(
    file_paths=['emergency_protocols.csv'],
    chunk_size=300,
    chunk_overlap=20
)

@CrewBase
class Agent7():
    """Emergency Guide crew"""
    
    @agent
    def emergency_guide_agent(self) -> Agent:
        return Agent(
            role="Agent de Guia d'Accions en Cas d'Emergència",
            goal="""Donar instruccions ràpides i precises als usuaris quan es detecta una emergència real.
                   Adaptar la resposta segons el tipus d'emergència.""",
            backstory="""Ets un agent especialitzat en gestió d'emergències, dissenyat per proporcionar 
                        instruccions clares i immediates en situacions de crisi. Tens coneixement 
                        exhaustiu dels protocols d'emergència per diferents escenaris i saps com 
                        comunicar-te de manera calmada i efectiva per evitar el pànic.""",
            llm=llm,
            memory=True,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": "john", 'local_mem0_config': config},
            },
            allow_delegation=False,
            max_iter=1,
            embedder=EMBEDDER_CONFIG,
        )

    @task
    def emergency_guidance_task(self) -> Task:
        return Task(
            description="""Fes servir l'historial de xat per construir la teva resposta a l'usuari:

                            {history}

                            Respon al missatge de l'usuari: {user_message} """,
            expected_output="""Tu respuesta debe ser relevante, precisa y clara, abordando directamente la consulta del usuario o continuando la conversación de manera lógica.
                                con el formato:
                            - Tipus d'emergència detectada
                            - Instruccions pas a pas adequades a la situació
                            - Punts clau de seguretat
                            - Indicacions sobre què evitar fer
                            - Informació sobre on buscar ajuda addicional""",
            agent=self.emergency_guide_agent()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the EmergencyGuide crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            max_rpm=20,
            knowledge_sources=[csv_source],
            embedder=EMBEDDER_CONFIG,
        )
