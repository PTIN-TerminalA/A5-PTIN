#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from agente12.crew import Agente12  # Asegúrate que esta ruta es correcta
 # Asegúrate que esta ruta es correcta

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Archivo principal para ejecutar el agente de información del aeropuerto
conversation_history = []


def run():
    """
    Ejecuta el agente en modo conversación interactiva.
    """
    while True:
        user_input = input("Tú: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Asistente: ¡Hasta luego! Fue un placer ayudarte.")
            break

        inputs = {
            'user_message': f"{user_input}",
        }

        try:
            response = Agente12().crew().kickoff(inputs=inputs)
        except Exception as e:
            raise Exception(f"Ocurrió un error al ejecutar el agente: {e}")

        print(f"Asistente: {response}")


def train():
    """
    Entrena el agente con un mensaje fijo.
    """
    inputs = {
        'user_message': '¿Qué servicios hay disponibles en el aeropuerto?',
    }

    try:
        Agente12().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"Ocurrió un error durante el entrenamiento: {e}")


def replay():
    """
    Reproduce una ejecución del agente desde una tarea específica.
    """
    try:
        Agente12().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"Ocurrió un error al reproducir la tarea: {e}")


def test():
    """
    Prueba la ejecución del agente con un mensaje de ejemplo.
    """
    inputs = {
        "user_message": "¿Dónde queda el Terminal A?",
        "current_year": str(datetime.now().year)
    }

    try:
        Agente12().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"Ocurrió un error durante la prueba: {e}")


if __name__ == "__main__":
    run()

