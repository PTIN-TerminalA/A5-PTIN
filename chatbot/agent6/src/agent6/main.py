def run():
    while True:
        user_input = input("You: ")

        inputs = {
            "user_message": user_input,
            # "session_id": sessio_id, ← opcional, pots controlar amb un history si vols
        }

        try:
            response = Agent3().crew().kickoff(inputs=inputs)
        except Exception as e:
            print(f"[ERROR] {e}")
            continue

        print(f"Assistant: {response}")
