from agent6.crew import Agent6
import uuid

def run():
    session_id = str(uuid.uuid4())  # Generem un UUID fix per la sessió
    crew = Agent6().crew()

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            print("Missatge buit. Torna a intentar-ho.")
            continue

         # Afegeix el context global per a totes les tasques (important)
        crew.context = {
            "user_message": user_input,
            "session_id": session_id
        }

        try:
            #response = Agent6().crew().kickoff(inputs=inputs)
             # Executem la crew amb les variables que l'agent necessita
            response = crew.kickoff(inputs={
                "user_message": user_input,
                "session_id": session_id
            })
        except Exception as e:
            print(f"[ERROR] {e}")
            continue

        print(f"Assistant: {response}")

if __name__ == "__main__":
    run()
