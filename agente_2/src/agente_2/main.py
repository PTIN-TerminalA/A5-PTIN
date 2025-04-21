#!/usr/bin/env python
import sys
import warnings
from agente_2.crew import Agent2
from datetime import datetime

warnings.filterwarnings("ignore", category=SyntaxWarning)

def run():
    print(">>> Agent activat. Esperant consulta...")
    while True:       
        user_input = input("Usuari: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Agent de Transport: Fins aviat! Bon viatge.")
            break

        inputs = {
            'user_message': f"{user_input}",
        }
        try:
            response = Agent2().crew().kickoff(inputs=inputs)
        except Exception as e:
            raise Exception(f"Error executant el crew: {e}")

        print(f"Agent de Transport: {response}")

def train():
    inputs = {
        'user_message': 'Com puc arribar a la terminal B des de la porta 15?',
    }
    try:
        Agent2().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"Error entrenant el crew: {e}")

def replay():
    try:
        Agent2().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"Error en replay del crew: {e}")

def test():
    inputs = {
        "topic": "transport intern aeroport",
        "current_year": str(datetime.now().year)
    }
    try:
        Agent2().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"Error testejant el crew: {e}")
    
if __name__ == "__main__":
    print(">>> Iniciant l'agent de transport")
    run()
