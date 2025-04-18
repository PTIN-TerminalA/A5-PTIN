#!/usr/bin/env python
import sys
import warnings

from agent3.crew import Agent3

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


conversation_history = []


def run():
    """
    Run the crew.
    """    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! It was nice talking to you.")
            break
        #conversation_history.append(f"User: {user_input}")
        #context = "\n".join(conversation_history[-3:])  # Usa los últimos 3 mensajes

        inputs = {
            'user_message': f"{user_input}",
        }
        try:
           response = Agent3().crew().kickoff(inputs=inputs)
        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}")

        conversation_history.append(f"Assistant: {response}")
        print(f"Assistant: {response}")






def train():
    """
    Train the crew for a given number of iterations.
    """
    
    inputs = {
        'user_message': 'Quins restaurants hi han?',
    }
    try:
        Agent3().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Agent3().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "aeropuerto assistente",
        "current_year": str(datetime.now().year)
    }
    try:
        Agent3().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
