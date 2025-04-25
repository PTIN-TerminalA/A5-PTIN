from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool
from crewai_tools import DirectorySearchTool

from typing import List, Optional

from dotenv import load_dotenv

from crewai import LLM

# Instancia del modelo LLM que se usará para los agentes
llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434", temperature=0.3)

# Herramienta que permite buscar información dentro de una carpeta local
tool = DirectorySearchTool(
    directory='knowledge/',  # Carpeta que contiene los documentos de conocimiento
    config=dict(
        llm=dict(
            provider="ollama",  # Modelo utilizado para la búsqueda
            config=dict(
                model="llama3.1",
                stream=True,
            ),
        ),
        embedder=dict(
            provider="ollama",  # Otras opciones de proveedor de embeddings
            config=dict(
                model="mxbai-embed-large",
            ),
        ),
    )
)

@CrewBase
class Agente12():
    """Crew de Información General del Aeropuerto"""

    # Ruta al archivo YAML donde están definidas las tareas
    tasks_config = 'config/tasks.yaml'

    # Definición de un agente para responder preguntas sobre servicios y otras consultas generales del aeropuerto
    @agent
    def agente_informacion_general(self) -> Agent:
        return Agent(
            role="Experto multilingüe en información general del aeropuerto",
            goal="""Responde a preguntas específicas sobre los servicios y operaciones del aeropuerto,
                proporcionando información clara y útil basada en los datos de los archivos CSV.
                Exprésate de manera natural, amigable y conversacional, como si estuvieras interactuando con una persona.
                Detecta automáticamente el idioma en que se formula la pregunta y responde en ese mismo idioma.
                Si la pregunta no se puede responder con los archivos CSV, dilo claramente y ofrece una alternativa si es posible.""",
            backstory="""Eres un experto en los servicios y operaciones de un aeropuerto con acceso a una base de datos
                        detallada en formato CSV. Tu objetivo es ayudar a los usuarios a encontrar respuestas rápidas y precisas.
                        Siempre respondes en el mismo idioma que utiliza la persona al preguntar (por ejemplo, español, inglés, etc.).""",
            llm=llm,  # Modelo de lenguaje a utilizar
            tools=[tool],  # Herramientas que el agente puede usar
            allow_delegation=False,  # No permite delegar tareas a otros agentes
            memory=True,  # Habilita la memoria (aunque no funcione completamente)
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            } 
        )

    # Definición de una tarea para responder preguntas, extraída del archivo YAML
    @task
    def informacion_terminalA(self) -> Task:
        return Task(
            config=self.tasks_config['informacion_terminalA'],  # Lee la configuración de esta tarea desde el archivo YAML
        )

    @task
    def servicios_disponibles(self) -> Task:
        return Task(
            config=self.tasks_config['servicios_disponibles'],  # Tarea de servicios disponibles
        )

    @task
    def horarios_areas_comerciales(self) -> Task:
        return Task(
            config=self.tasks_config['horarios_areas_comerciales'],  # Tarea de horarios de áreas comerciales
        )

    @task
    def estado_vuelos(self) -> Task:
        return Task(
            config=self.tasks_config['estado_vuelos'],  # Tarea de estado de vuelos
        )

    @task
    def consulta_general(self) -> Task:
        return Task(
            config=self.tasks_config['consulta_general'],  # Tarea de consulta general
        )

    @crew
    def crew(self) -> Crew:
        """Crea el crew del Agente12"""
        return Crew(
            agents=self.agents,  # Agentes automáticamente creados por el decorador @agent
            tasks=self.tasks,  # Tareas automáticamente creadas por el decorador @task
            process=Process.sequential,  # Las tareas se ejecutan una tras otra
            verbose=True,  # Muestra información detallada de la ejecución
            memory=True,  # Habilita la memoria para todo el crew
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }
            }, 
        )