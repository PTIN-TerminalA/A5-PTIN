from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List, Optional
from crewai_tools import MySQLSearchTool

from dotenv import load_dotenv

from crewai import LLM


# Instància del model LLM que s’utilitzarà per als agents
llm= LLM(model="ollama/llama3.1", base_url="http://localhost:11434", temperature=0.3)

# Eina que permet buscar informació dins de una base de dades mysql.
tool = MySQLSearchTool(
    table_name='vuelos',
    db_config={
        'host': 'x',
        'port': 3306,
        'user': 'x,
        'password': 'x',
        'database': 'x',
    },
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
    def qa_agent(self) -> Agent:
        return Agent(
           # config=self.agents_config['agente_servicios_comerciales'],
            role="Experto multilingüe en Estado del Vuelo dentro de un sistema inteligente distribuido para la gestión de información aeroportuaria en tiempo real.",
            goal="""Resolver dudas generales o específicas relacionadas con vuelos identificados por número, compañía o destino.
                    basada en los datos de la base de datos proporcionada.
                    Exprésate de manera natural, amigable y conversacional, como si hablaras con una persona.
                    Detecta automáticamente el idioma en que se formula la pregunta y responde en ese mismo idioma.
                    Si la pregunta no se puede responder con la base de datos, dilo claramente.""",
            backstory="""Eres el Agente de Estado del Vuelo dentro de un sistema inteligente distribuido para la gestión de información aeroportuaria en tiempo real.
                        Tu misión es proporcionar información precisa, fiable y actualizada sobre cualquier vuelo programado en el aeropuerto, respondiendo de forma rápida y 
                        clara a las consultas de los pasajeros o del personal del recinto.
                        Siempre respondes en el mismo idioma que usa la persona al preguntar (por ejemplo, español, inglés o catalán).""",
            llm=llm, # Model de llenguatge a utilitzar
            tools=[tool], # Llista d’eines que pot fer servir
            allow_delegation=False, # No permet delegar tasques a altres agents
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
    def answer_question_task(self) -> Task:
        return Task(
            config=self.tasks_config['answer_question_task'], # Llegeix la configuració d’aquesta tasca des del fitxer YAML
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Agent4 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential, # Les tasques s’executen una darrere l’altra
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