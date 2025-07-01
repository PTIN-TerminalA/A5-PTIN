#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from agent4.crew import Agent4

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():

    history = [] 
    while True:
        # Mostra el prompt i recull l’entrada de l’usuari
        user_input = input("john: ")

        # Si l’usuari escriu alguna d’aquestes paraules, es finalitza la sessió
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! It was nice talking to you.")
            break
        
        chat_history = "\n".join(history[-2:]) if len(history) >= 2 else ""

        # Prepara les dades d’entrada per al crew
        inputs = {
            "user_message": f"{user_input}",
             "history": f"{chat_history}",
        }

        response = Agent4().crew().kickoff(inputs=inputs)

        history.append(f"User: {user_input}")
        history.append(f"Assistant: {response}")

        print(f"Assistant: {response}")



def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Agent4().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Agent4().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        Agent4().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
