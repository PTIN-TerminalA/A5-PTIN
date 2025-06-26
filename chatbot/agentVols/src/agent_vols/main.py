#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from mem0 import MemoryClient

from agent_vols.crew import AgentVols

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():

    history = []    
    while True:
        
        # Mostra el prompt i recull l’entrada de l’usuari
        user_input = input("You: ")

        # Si l’usuari escriu alguna d’aquestes paraules, es finalitza la sessió
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! It was nice talking to you.")
            break
        
        chat_history = "\n".join(history[-2:]) if len(history) >= 2 else ""

        # Prepara les dades d’entrada per al crew
        inputs = {
            "user_id": 64,
            "user_message": f"{user_input}",
             "history": f"{chat_history}",
        }

        response = AgentVols().kickoff(inputs=inputs)

        history.append(f"User: {user_input}")
        history.append(f"Assistant: {response}")

        print(f"Assistant: {response}")


def train():
    """
    Entrena l'agent per a un cas concret de prova.
    """
    inputs = {
        'user_id': 1,
        'user_message': 'Quan surt el meu vol?',
        'history': ''
    }
    try:
        AgentVols().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"Error durant l'entrenament: {e}")


def replay():
    """
    Reprodueix una execució anterior per depurar.
    """
    try:
        AgentVols().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"Error durant la repetició: {e}")


def test():
    """
    Test de l'agent per veure com respon.
    """
    inputs = {
        'user_id': 1,
        'user_message': 'Quina porta tinc?',
        'history': ''
    }
    try:
        AgentVols().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"Error durant el test: {e}")