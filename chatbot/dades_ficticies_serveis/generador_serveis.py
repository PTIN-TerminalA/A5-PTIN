from faker import Faker
import random
import pandas as pd

# Instàncies de Faker per diferents cultures
faker_es = Faker('es_ES')
faker_it = Faker('it_IT')
faker_fr = Faker('fr_FR')
faker_en = Faker('en_US')

# Tipologies i formats de noms per cada una
tipologies = {
    'Restaurant': {
        'Cuina italiana': [
            "Trattoria {nom}",
            "Pasta & {nom}",
            "La Tavola di {nom}",
            "Cuina Italiana {ciutat}",
            "Ristorante {nom}",
            "{nom} al Forno",
            "Sapore di {ciutat}",
            "Roma Cuina",
            "Gust Toscà",
            "Napoli Express"
        ],
        'Cuina ràpida': [
            "Fast & {nom}",
            "{nom} Express",
            "Bocateria {nom}",
            "QuickBite {ciutat}",
            "Menjar Ràpid {ciutat}",
            "Delit Ràpid",
            "SnackTime {nom}",
            "Street Food {ciutat}",
            "Go! {nom}",
            "Food Stop"
        ],
        'Mediterrània': [
            "Gust Mediterrani",
            "Sabors de {ciutat}",
            "El Racó del Mar",
            "Delícies de {ciutat}",
            "Mediterrània {nom}",
            "Cuina del Sud",
            "Sabors & Olives",
            "La Taula del Sol",
            "Sabor d’Estiu",
            "Taverna Mediterrània"
        ],
        'Cafeteria': [
            "Cafeteria {nom}",
            "Espresso {ciutat}",
            "{nom} Coffee",
            "La Tassa de {nom}",
            "Café Central",
            "Racó Cafè",
            "Bon Cafè {ciutat}",
            "Coffee & {nom}",
            "Latte Time",
            "Bar {nom}"
        ]
    },
    'Botiga': {
        'Moda': [
            "Moda {nom}",
            "Tendències {ciutat}",
            "Style & {nom}",
            "Vestir Bé",
            "Urban Look",
            "Chic {ciutat}",
            "Moda&Cia",
            "Estil {nom}",
            "LookBook",
            "Elegant Life"
        ],
        'Perfumeria': [
            "Essències de {ciutat}",
            "{nom} Perfums",
            "Aromes {nom}",
            "Perfumis",
            "Olor Natural",
            "Fragància & Co",
            "Elixir {ciutat}",
            "Scents {nom}",
            "L’essència de {nom}",
            "Perfumeria Selecta"
        ],
        'Premsa i llibres': [
            "Llibres {nom}",
            "Lectura+ {ciutat}",
            "Temps de Lectura",
            "Relay",
            "Punt de Llibres",
            "Lectura Global",
            "Book Stop",
            "Revistes & Co",
            "Llibres Viatgers",
            "Espai de Lectura"
        ],
        'Productes naturals': [
            "Natura {ciutat}",
            "EcoMarket {nom}",
            "Verda Vida",
            "NaturalMente",
            "Biosfera",
            "El Racó Verd",
            "Organic Shop",
            "Salut Natural",
            "Vida Eco",
            "Botiga Bio {ciutat}"
        ]
    }
}

# Preus segons la tipologia
preus_per_tipologia = {
    'Cuina italiana': ['€€', '€€€'],
    'Cuina ràpida': ['€'],
    'Mediterrània': ['€€'],
    'Cafeteria': ['€', '€€'],
    'Moda': ['€€', '€€€'],
    'Perfumeria': ['€€', '€€€'],
    'Premsa i llibres': ['€', '€€'],
    'Productes naturals': ['€', '€€']
}

ubicacions = [f"Terminal {t} - Porta {p}" for t in ['A'] for p in range(1, 30)]
horaris = ['06:00–22:00', '09:00–21:00', '10:00–20:00', '07:00–23:00']
noms_usats = set()

# Selecció de Faker segons la tipologia
def faker_per_tipologia(tipologia):
    if tipologia == 'Cuina italiana':
        return faker_it
    elif tipologia in ['Moda', 'Perfumeria']:
        return faker_fr
    elif tipologia in ['Premsa i llibres', 'Productes naturals', 'Cuina ràpida', 'Mediterrània', 'Cafeteria']:
        return faker_es
    else:
        return faker_en

# Generació de nom + categoria + tipologia (sense repetir noms)
def generar_nom_tipologia_categoria():
    categoria = random.choice(list(tipologies.keys()))
    tipologia = random.choice(list(tipologies[categoria].keys()))
    formats = tipologies[categoria][tipologia]
    faker_local = faker_per_tipologia(tipologia)

    intents = 0
    while True:
        plantilla = random.choice(formats)
        nom = faker_local.first_name()
        ciutat = faker_local.city()
        nom_final = plantilla.format(nom=nom, ciutat=ciutat)

        if nom_final not in noms_usats:
            noms_usats.add(nom_final)
            return nom_final, categoria, tipologia

        intents += 1
        if intents > 1000:
            raise Exception("No es poden generar més noms únics!")

# Generació de dades
data = []

for _ in range(100):
    nom, categoria, tipologia = generar_nom_tipologia_categoria()
    ubicacio = random.choice(ubicacions)
    horari = random.choice(horaris)
    preu = random.choice(preus_per_tipologia[tipologia])

    data.append([nom, categoria, tipologia, ubicacio, horari, preu])

# Exportació a CSV
df = pd.DataFrame(data, columns=['Nom', 'Categoria', 'Tipologia', 'Ubicació', 'Horari', 'Preu'])
df.to_csv("dades_serveis.csv", index=False)

print(df.head())
