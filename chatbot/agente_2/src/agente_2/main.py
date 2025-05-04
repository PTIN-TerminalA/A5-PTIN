#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from agente_2.crew import Agent2

warnings.filterwarnings("ignore", category=SyntaxWarning)

def run():
    print(">>> Agent de Transport activat.")
    history = []

    while True:
        user_input = input("Usuari: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Agent de Transport: Fins aviat! Bon viatge.")
            break

        chat_history = "\n".join(history[-4:]) if len(history) >= 4 else ""
        inputs = {
            'user_message': user_input,
            'history': chat_history
        }

        try:
            response = Agent2().crew().kickoff(inputs=inputs)
        except Exception as e:
            print(f"Error: {e}")
            continue

        history.append(f"Usuari: {user_input}")
        history.append(f"Agent: {response}")
        print(f"Agent de Transport: {response}")

def train():
    inputs = {
        'user_message': 'Com arribo de la porta 10 a la Terminal A?',
    }
    try:
        Agent2().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        print(f"Error entrenant el crew: {e}")

def replay():
    try:
        Agent2().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        print(f"Error fent replay del crew: {e}")

def test():
    inputs = {
        "topic": "transport intern aeroport",
        "current_year": str(datetime.now().year)
    }
    try:
        Agent2().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        print(f"Error testejant el crew: {e}")

if __name__ == "__main__":
    run()
