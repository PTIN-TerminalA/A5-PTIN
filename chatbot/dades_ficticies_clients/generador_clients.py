from faker import Faker
import random
import pandas as pd

fake = Faker('es_ES')

# Llista de tipologies comercials de l'aeroport (fet sobre generador_serveis)
tipologies_existents = [
    'Cuina italiana', 'Cuina ràpida', 'Mediterrània', 'Cafeteria',
    'Moda', 'Perfumeria', 'Premsa i llibres', 'Productes naturals'
]

perfils_viatge = ['Negocis', 'Turisme', 'Família', 'Altres']
interaccions = [
    'Accepta ofertes de menjar',
    'Ignora promocions',
    'Respon a ofertes de llibres',
    'Segueix suggeriments personalitzats',
    'Només consulta horaris i ubicacions'
]

def generar_preferencies():
    return ', '.join(random.sample(tipologies_existents, random.randint(1, 3)))

def generar_historial():
    serveis = ['restaurants', 'botigues', 'vehicles', 'cafeteries', 'llibres']
    interaccions = []
    for s in random.sample(serveis, k=random.randint(1, 3)):
        n = random.randint(1, 5)
        interaccions.append(f"{n} {'consulta' if n == 1 else 'consultes'} a {s}")
    return ', '.join(interaccions)

# Generació de clients
clients = []

for i in range(1, 3001):
    id_client = f"{i:04}"
    genere = random.choice(['F', 'M'])

    if genere == 'F':
        nom = fake.first_name_female() + ' ' + fake.last_name()
    else:
        nom = fake.first_name_male() + ' ' + fake.last_name()

    edat = random.randint(18, 75)
    perfil = random.choice(perfils_viatge)
    preferencies = generar_preferencies()
    interaccio = random.choice(interaccions)
    historial = generar_historial()

    clients.append([
        id_client, nom, edat, genere, perfil,
        preferencies, interaccio, historial
    ])

# Crear DataFrame i exportar a CSV
df = pd.DataFrame(clients, columns=[
    'ID client', 'Nom', 'Edat', 'Gènere', 'Perfil de viatge',
    'Preferències comercials', 'Interacció habitual', 'Historial d’usos'
])

df.to_csv("clients_ficticis.csv", index=False)

print(df.head())
