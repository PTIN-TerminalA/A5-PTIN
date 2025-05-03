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
            "collection_name": "agent3",
            "host": "192.168.10.12",
            "port": 6333,
            "embedding_model_dims": 768,  # Change this according to your local model's dimensions
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.1:latest",
            "temperature": 0,
            "max_tokens": 2000,
            "ollama_base_url": "http://192.168.10.12:11434",  # Ensure this URL is correct
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text:latest",
            # Alternatively, you can use "snowflake-arctic-embed:latest"
            "ollama_base_url": "http://192.168.10.12:11434",
        },
    },
}


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Instància del model LLM que s’utilitzarà per als agents
llm = LLM(
    model="ollama/llama3.1",  # Versión más ligera
    base_url="http://192.168.10.12:11434",
    temperature=0.3,
    config={
        "max_tokens": 200,  # Limita respuesta
        "top_k": 10         # Reduce opciones de sampling
    }
)



# Eina que permet buscar informació dins d’una carpeta local
# tool = CSVSearchTool(
#      csv='knowledge/dades_serveis.csv', # Carpeta que conté els documents de coneixement
#      config=dict(
#          llm=dict(
#              provider="ollama", # or google, openai, anthropic, llama2, ...
#              config=dict(
#                  model="llama3.1",
#                  stream=True,
#              ),
#          ),
#          embedder=EMBEDDER_CONFIG,
#      )
#  )

csv_source = CSVKnowledgeSource(
    file_paths=['dades_serveis.csv','punts_importants_aeroport.csv'],
    chunk_size=300,      # Maximum size of each chunk (default: 4000)
    chunk_overlap=20
)



@CrewBase
class Agent3():
    """Agent3 crew"""
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
   # agents_config = 'config/agents.yaml'

    # Ruta al fitxer YAML on estan definides les tasques
    #tasks_config = 'config/tasks.yaml'


    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    # Definició d’un agent que farà preguntes i respostes sobre serveis d’aeroport
    @agent
    def asistente_servicios(self) -> Agent:
        return Agent(
            role="Asistente Virtual de Aeropuerto",
            goal="""Brindar respuestas precisas, útiles y claras sobre los servicios disponibles en el aeropuerto, mejorando la experiencia del usuario y resolviendo sus dudas de forma rápida y eficiente. """,
            backstory="""Eres un asistente virtual avanzado, especializado en información aeroportuaria. Estás diseñado para ayudar a los pasajeros con preguntas sobre servicios como tiendas, restaurantes, salas VIP y más.
            Aunque no tienes experiencias ni emociones humanas, estás programado para responder con empatía, cortesía y lenguaje claro, adaptándote al estilo de cada usuario.
            Siempre buscas ofrecer información actualizada y relevante, y reconoces con honestidad cuando un tema está fuera de tu alcance o requiere asistencia humana.""",
            llm=llm, # Model de llenguatge a utilitzar
            #tools=[tool], # Llista d’eines que pot fer servir
            #knowledge_sources=[csv_source],
            memory=True,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": "john", 'local_mem0_config': config},
            },
            allow_delegation=False, # No permet delegar tasques a altres agents
            max_iter=1,
            embedder=EMBEDDER_CONFIG,
        )


    # Definició d’una tasca per respondre preguntes
    @task
    def task_chat_service(self) -> Task:
        return Task(
            description="""Usa el historial de conversación para construir tu respuesta al usuario:

                            {history}

                            Responde al mensaje del usuario: {user_message} """,
            expected_output="""Tu respuesta debe ser relevante, precisa y clara, abordando directamente la consulta del usuario o continuando la conversación de manera lógica.
                                con el formato:
                                - Nombre del establecimiento
                                - Ubicación exacta (terminal y puerta)
                                - Horario
                                - Rango de precio (si aplica).""",
           agent=self.asistente_servicios()
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Agent3 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,  # Mejor que sequential
            max_rpm=20, # Les tasques s’executen una darrere l’altra
            #verbose=True,  # Mostra informació detallada de l’execucio 
            knowledge_sources=[csv_source],
            embedder=EMBEDDER_CONFIG,
              
        )
