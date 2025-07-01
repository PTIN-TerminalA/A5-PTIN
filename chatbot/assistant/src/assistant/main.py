#!/usr/bin/env python
# from random import randint
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
import csv

from assistant.crews.api.api import api
from assistant.crews.service.service import service
from assistant.crews.flights.flights import flights, getDatosVuelos
from assistant.crews.central.central import central

class UserInput(BaseModel):
    input: str = ""

class MainFlow(Flow[UserInput]):

    @start()
    def get_user_input(self):
        # print("Starting flow")
        # self.state.input = input("You:")
        self.state.input = "Hola! Donde puedo comer?"
        #self.state.input = "Hey! I want to rent a car?"
        #self.state.input = "Hey! I want to know about my flights!"
        return self.state.input

    @listen(get_user_input)
    def start_conversation(self):
        history = []

        history = "\n".join(history[-2:]) if len(history) >= 2 else ""

        inputs = {
            "user_id": 64,
            "history": f"{history}",
            "user_message": self.state.input,
        }

        response = ""

        try:
            # decision = central().crew().kickoff(inputs=inputs)
            raw = central().crew().kickoff(inputs=inputs)
            # print(decision)
            decision = raw["classified"]
            language = raw["language"]
            inputs["language"] = language
            # print(inputs)
        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}")

        if decision == 'commerce':
            try:
                response = service().crew().kickoff(inputs=inputs)
            except Exception as e:
                raise Exception(f"An error occurred while running the crew: {e}")
        elif decision == 'car':
            try:
                store_names = set()
                with open("/home/iaa/assistant/knowledge/services.csv", newline='', encoding='utf-8') as archivo_csv:
                    lector = csv.DictReader(archivo_csv)
                    for fila in lector:
                        store_names.add(fila['name'].lower())
                user_message = input("You: ").strip().lower()
                exists = False
                while not exists:
                    for store in store_names:
                        if store in user_message:
                            print(f"OK")
                            response = api().crew().kickoff(inputs=inputs)
                            exists = True
                            break
                    if not exists:
                        print("Botiga no trobada. Si us plau, tria una d'aquestes opcions:")
                        print(", ".join(store_names))
                        user_message = input("You: ").strip().lower()
                
            except Exception as e:
                raise Exception(f"An error occurred while running the crew: {e}")
        elif decision == 'flights':
            try:
                flight_info = getDatosVuelos(inputs.get("user_id", 0))
             
                if isinstance(flight_info, str):
                    # Si no hi ha dades del vol
                    inputs["flight_info"] = flight_info
                else:
                    # Interpretem valors booleans com a text comprensible
                    flight_info["is_canceled"] = "Sí" if flight_info["is_canceled"] else "No"
                    flight_info["is_delayed"] = "Sí" if flight_info["is_delayed"] else "No"
                    inputs["flight_info"] = "\n".join(f"{k}: {v}" for k, v in flight_info.items())
                
                response = flights().crew().kickoff(inputs=inputs)
            except Exception as e:
                raise Exception(f"An error occurred while running the crew: {e}")
        else:
            print("There's a problem.")


        print(response)
        # history.append(f"User: {self.state.input}")
        # history.append(f"Assistant: {response}")

def kickoff():
    flow = MainFlow(UserInput())
    flow.kickoff()

if __name__ == "__main__":
    kickoff()
