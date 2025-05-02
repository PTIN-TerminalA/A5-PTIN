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
            "collection_name": "agent11",
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



# Eina que permet buscar informació dins d’una carpeta local
# tool = CSVSearchTool(
#      csv='knowledge/protocols_incidencies.csv', # Carpeta que conté els documents de coneixement
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
    file_paths=['protocols_incidencies.csv'],
    chunk_size=300,      # Maximum size of each chunk (default: 4000)
    chunk_overlap=20
)


@CrewBase
class Agent11():
    """Agent1 crew"""
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
    def agent_protocols(self) -> Agent:
    	return Agent(
        	role="Agent de Protocols en cas d’Incidència",
        	goal="""Ajudar l’usuari a saber què ha de fer davant d’incidències comunes en el context d’un aeroport, com ara la pèrdua d’equipatge o de vols, problemes amb documents, etc.""",
       		backstory="""Ets un agent virtual especialitzat en protocols d’assistència davant incidències no greus però rellevants a l’aeroport.
        	Estàs dissenyat per guiar els viatgers amb informació clara, concreta i directa sobre què fer en cada situació.
        	Detectes el tipus de problema que expressa l’usuari i ofereixes els passos a seguir, punts de contacte, i recomanacions útils.
        	No gestiones emergències de seguretat, sinó incidències habituals com errors de reserva, documents, o pèrdua d’equipatge.
        	Pots fer preguntes per adaptar millor la resposta si cal, i sempre et comuniques amb empatia i precisió.""",
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



    # Definició d’una tasca per respondre preguntes
    @task
    def task_protocols(self) -> Task:
        return Task(
            description="""Fes servir l'historial de xat per construir la teva resposta a l'usuari:

                            {history}

                            Respon al missatge de l'usuari: {user_message} """,
            expected_output="""Tu respuesta debe ser relevante, precisa y clara, abordando directamente la consulta del usuario o continuando la conversación de manera lógica.
                                con el formato:
                                - Tipus d’incidència detectada
                                - Instruccions pas a pas
                                - Telèfons o punts de contacte rellevants
                                - Pregunta addicional si és necessària per oferir millor ajuda""",
           agent=self.agent_protocols()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Agent11 crew"""
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