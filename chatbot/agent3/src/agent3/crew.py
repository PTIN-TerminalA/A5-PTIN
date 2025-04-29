from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool
from crewai_tools import DirectorySearchTool
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from crewai.tools import tool
import pandas as pd
import json
from typing import List, Optional

from dotenv import load_dotenv

from crewai import LLM




# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Instància del model LLM que s’utilitzarà per als agents
llm = LLM(
    model="ollama/llama3",  # Versión más ligera
    base_url="http://localhost:11434",
    temperature=0.3,
    config={
        "max_tokens": 500,  # Limita respuesta
        "top_k": 30         # Reduce opciones de sampling
    }
)


@tool("csv_reader_tool")
def csv_reader_tool(query: str) -> str:
    """Lee datos de un archivo CSV y devuelve información específica."""
    try:
        if isinstance(query, str):
        query = json.loads(query)

        # 2. Extraer la parte importante
        user_query = query.get('query', {}).get('description', '')

        df = pd.read_csv('knowledge/dades_serveis.csv')
        mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(real_query.lower()).any(), axis=1)
        results = df[mask]
        
        if results.empty:
            return "No se encontraron servicios que coincidan con tu búsqueda."

        return "\n\n".join([
            f"Nombre: {row['Nom']}\n"
            f"Categoría: {row['Categoria']}\n"
            f"Tipo: {row['Tipologia']}\n"
            f"Ubicación: {row['Ubicació']}\n"
            f"Horario: {row['Horari']}\n"
            f"Precio: {row['Preu']}"
            for _, row in results.iterrows()
        ])
    except Exception as e:
        return f"Error al leer el archivo CSV: {str(e)}"



# Eina que permet buscar informació dins d’una carpeta local
# tool = CSVSearchTool(
#     csv='knowledge/dades_serveis.csv', # Carpeta que conté els documents de coneixement
#     config=dict(
#         llm=dict(
#             provider="ollama", # or google, openai, anthropic, llama2, ...
#             config=dict(
#                 model="llama3",
#                 #cache=True,
#                 #top_k=30,    
#                 #max_tokens=2000, 
#                 # temperature=0.5,
#                 # top_p=1,
#                 stream=True,
#             ),
#         ),
#         embedder=dict(
#             provider="ollama", # or openai, ollama, ...
#             config=dict(
#                 model="mxbai-embed-large",
#                 # title="Embeddings",
#             ),
#         ),
#     )
# )


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
    def service_finder(self) -> Agent:
        return Agent(
           # config=self.agents_config['agente_servicios_comerciales'],
            role="Buscador de servicios del Aeropuerto",
            goal="""Encontrar servicios del aeropuerto basados en las preguntas de los usuarios""",
            backstory="""Especialista en la información de todos los servicios disponibles en el aeropuerto""",
            llm=llm, # Model de llenguatge a utilitzar
            #tools=[tool], # Llista d’eines que pot fer servir
            tools=[csv_reader_tool],
            allow_delegation=False, # No permet delegar tasques a altres agents
            max_iter=3,
            memory=True, # Activa la memòria (encara que no funciona del tot correctament en aquesta versió)
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            } 
        )

    @agent
    def response_generator(self) -> Agent:
        return Agent(
            role="Generador de Respuestas Amigables",
            goal="Generar respuestas claras y completas sobre los servicios del aeropuerto",
            backstory="Experto en brindar respuestas rápidas, claras y amables a los pasajeros, siempre tambien.",
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            memory=True, # Activa la memòria (encara que no funciona del tot correctament en aquesta versió)
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            }
    )

    # Definició d’una tasca per respondre preguntes, extreta d’un YAML
    @task
    def task_find_service(self) -> Task:
        return Task(
            description="""Busca en la información del aeropuerto detalles relevantes que respondan a la pregunta: '{user_message}'.
                        Teniendo como referencia el documento csv dades_serveis.csv """,
            expected_output="""Servicio o servicios encontrados que coincidan con la necesidad del usuario.
                                Si la información solicitada no se encuentra en el archivo, indica educadamente que no se dispone de datos al respecto. """,
           agent=self.service_finder()
        )

    @task
    def task_generate_response(self) -> Task:
        return Task(
            description="""Redacta una respuesta clara y amigable basada en la información encontrada por el Buscador de Servicios.
            IMPORTANTE: Genera la respuesta en el idioma del usuario: '{language}'.""",
            expected_output="""Respuesta final en el idioma solicitado.""",
            agent=self.response_generator(), 
            context=[self.task_find_service()]
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
            max_rpm=10, # Les tasques s’executen una darrere l’altra
           # knowledge_sources=[self.csv_source],
            verbose=True,  # Mostra informació detallada de l’execució
            memory=True,  # Activa la memòria per a tot el crew (no funciona 100% bé actualment)
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            }, 
              
        )