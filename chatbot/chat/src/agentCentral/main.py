#!/usr/bin/env python
import sys
import warnings
import csv

from agentCentral.crew import ChatBot

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

conversation_history = []

# Carrega els usuaris en un diccionari nom → user_id
def carregar_usuaris(path="knowledge/taula_user.csv"):
    usuaris = {}
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            nom = fila["nom"].strip().lower()
            usuari_id = fila["id"].strip()
            usuaris[nom] = usuari_id
    return usuaris

# Crida la funció una vegada
mapa_usuaris = carregar_usuaris()

def run():
    """
    Run the crew.
    """    
    
    print("Welcome! Say your name to start:")
    nom_usuari = input("Name: ").strip().lower()
    user_id = mapa_usuaris.get(nom_usuari, "default")

    if user_id == "default":
        print("This user has not been found in the system. A default ID will be used.")

    while True:
        # Mostra el prompt i recull l’entrada de l’usuari
        user_input = input("You: ")

        # Si l’usuari escriu alguna d’aquestes paraules, es finalitza la sessió
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! It was nice talking to you.")
            break
        # Afegeix a l’historial
        conversation_history.append(f"User: {user_input}")
        context = "\n".join(conversation_history[-3:])  # Usa los últimos 3 mensajes

        # Prepara les dades d’entrada per al crew
        inputs = {
            'user_message': f"{user_input}",
            'history': context,
            "user_id": user_id
        }
        try:
             # Crea una nova instància del crew i l’executa amb les dades d’entrada
           response = ChatBot().crew().kickoff(inputs=inputs)
        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}")

        conversation_history.append(f"Assistant: {response}")
        # Mostra la resposta per pantalla
        print(f"Assistant: {response}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    
    inputs = {
        'user_message': 'Quins restaurants hi han?',
    }
    try:
        ChatBot().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ChatBot().crew().replay(task_id=sys.argv[1])

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
        ChatBot().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
