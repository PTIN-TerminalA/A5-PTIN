from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List, Optional
from crewai_tools import MySQLSearchTool
import mysql.connector
from dotenv import load_dotenv
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource



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
            "collection_name": "agent4",
            "host": "localhost",
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
            "ollama_base_url": "http://localhost:11434",  # Ensure this URL is correct
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text:latest",
            # Alternatively, you can use "snowflake-arctic-embed:latest"
            "ollama_base_url": "http://localhost:11434",
        },
    },
}


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Instància del model LLM que s’utilitzarà per als agents
llm = LLM(
    model="ollama/llama3.1",  # Versión más ligera
    base_url="http://localhost:11434",
    temperature=0.3,
    config={
        "max_tokens": 200,  # Limita respuesta
        "top_k": 10         # Reduce opciones de sampling
    }
)


# Eina que permet buscar informació dins de una base de dades mysql.
# tool = MySQLSearchTool(
#     table_name='vuelos',
#     db_config={
#         'host': 'ubiwan.epsevg.upc.edu',
#         'port': 3306,
#         'user': 'x',
#         'password': 'x',
#         'database': 'x',
#     },
#     config=dict(
#         llm=dict(
#             provider="ollama", # or google, openai, anthropic, llama2, ...
#             config=dict(
#                 model="llama3.1",
#                 #top_k=50,    
#                 #max_tokens=2000, 
#                 # temperature=0.5,
#                 # top_p=1,
#                 stream=True,
#             ),
#         ),
#         embedder=dict(
#             provider="ollama", # or openai, ollama, ...
#             config=dict(
#                 model="nomic-embed-text",
#                 # title="Embeddings",
#             ),
#         ),
#     )
# )

# Funció que es una connecta a una base de dades, agafa totes les dades de una taula i la pasa a string per a que
#el agent el pugui analitzar.
def obtener_datos():
    conn = mysql.connector.connect(
        host="ubiwan.epsevg.upc.edu",
        user="x",
        password="x",
        database="x"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vuelos")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

datos = obtener_datos()

contenido = "\n".join([
    f"{fila[0]} - {fila[1]} - {fila[2]} - {fila[3]} - {str(fila[4])} - {fila[5]} - {fila[6]} - {fila[7]}"
    for fila in datos
])

string_source = StringKnowledgeSource(
    content=contenido,
    chunk_size=300,      # Maximum size of each chunk (default: 4000)
    chunk_overlap=20
)

@CrewBase
class Agent4():
    """Agent4 crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
   # agents_config = 'config/agents.yaml'

    # Ruta al fitxer YAML on estan definides les tasques
    tasks_config = 'config/tasks.yaml'


    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    # Definició d’un agent que farà preguntes i respostes sobre serveis d’aeroport
    @agent
    def asistente_vuelos(self) -> Agent:
        return Agent(
           # config=self.agents_config['agente_servicios_comerciales'],
            role="Asistente Virtual de Información de Vuelos",
            goal="""Brindar información precisa, clara y actualizada sobre vuelos, incluyendo horarios, puertas de embarque, retrasos, cancelaciones y conexiones, para ayudar a los pasajeros a planificar su viaje de forma eficiente y reducir su incertidumbre.""",
            backstory = """Eres un asistente virtual avanzado, especializado en brindar información sobre vuelos. Estás diseñado para asistir a los pasajeros con dudas relacionadas con salidas, llegadas, estatus de vuelos, conexiones, cambios de última hora y otros detalles relevantes.
            Aunque no tienes experiencias ni emociones humanas, estás programado para comunicarte con empatía, cortesía y un lenguaje accesible, adaptándote al tono de cada usuario.
            Siempre priorizas ofrecer datos en tiempo real y reconoces con honestidad cuando una consulta requiere intervención humana o acceso a sistemas específicos de las aerolíneas.""",
            llm=llm, # Model de llenguatge a utilitzar
            #tools=[tool], # Llista d’eines que pot fer servir
            memory=True,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": "john", 'local_mem0_config': config},
            },
            allow_delegation=False, # No permet delegar tasques a altres agents
            max_iter=1,
            embedder=EMBEDDER_CONFIG,
        )

    # Definició d’una tasca per respondre preguntes, extreta d’un YAML
    @task
    def task_chat_vuelos(self) -> Task:
        return Task(
            description="""Usa el historial de conversación para construir tu respuesta al usuario:

                            {history}

                            Responde al mensaje del usuario: {user_message} """,
            expected_output="""Tu respuesta debe ser relevante, precisa y clara, abordando directamente la consulta del usuario o continuando la conversación de manera lógica.
                                con el formato:
                                - id
                                - numero vuelo
                                - Compañia
                                - Destino
                                - Hora salida
                                - Puerta
                                - Estado """,
            agent=self.asistente_vuelos()
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Agent4 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,  # Mejor que sequential
            knowledge_sources=[string_source],
            max_rpm=20, # Les tasques s’executen una darrere l’altra
            #verbose=False,  # Mostra informació detallada de l’execucio 
            #knowledge_sources=[csv_source],
            embedder=EMBEDDER_CONFIG,
              
        )