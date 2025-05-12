from faker import Faker  # pip install faker
from unidecode import unidecode  # pip install unidecode
import random
from datetime import datetime
import csv

fake = Faker('es_ES')

# Per emmagatzemar les dades generades
usuaris = []
regulars = []
genders = set()

# Per controlar IDs autoincrementals (simulat)
current_id = 1

# Funció per generar correu electrònic a partir del nom
def generar_email(nom_complet):
    nom_sense_accents = unidecode(nom_complet.lower())
    parts = nom_sense_accents.split()

    nom = parts[0]
    cognom = parts[1] if len(parts) > 1 else "usuari"

    opcions = [
        f"{nom}{cognom}@gmail.com",
        f"{nom[0]}{cognom}@gmail.com",
        f"{nom}{cognom[0]}@gmail.com",
        f"{nom}.{cognom}@gmail.com",
        f"{cognom}{random.randint(1,99)}@gmail.com"
    ]
    return random.choice(opcions)

# Funció per generar un DNI amb lletra vàlida
def generar_dni_valid():
    numero = fake.unique.random_number(digits=8)
    lletra = "TRWAGMYFPDXBNJZSQVHLCKE"[numero % 23]
    return f"{numero:08d}{lletra}"

# Funció per formatar el número de telèfon a +34 123456789
def formatar_telefon(numero):
    digits = ''.join(filter(str.isdigit, numero))
    if digits.startswith('34'):
        digits = digits[2:]
    elif digits.startswith('0034'):
        digits = digits[4:]
    return f"+34 {digits}"

for _ in range(3000):
    user_id = current_id
    current_id += 1

    # Nom i gènere
    genere = random.choice(['F', 'M'])
    genders.add(genere)
    if genere == 'F':
        nom = fake.first_name_female() + ' ' + fake.last_name()
    else:
        nom = fake.first_name_male() + ' ' + fake.last_name()

    # Dades usuari
    dni = generar_dni_valid()
    email = generar_email(nom)
    password = fake.password(length=12)
    usertype = 1  # regular

    usuaris.append({
        "id": user_id,
        "name": nom,
        "dni": dni,
        "email": email,
        "password": password,
        "usertype": usertype
    })

    # Dades regular
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=75)
    phone_raw = fake.phone_number()
    phone_num = formatar_telefon(phone_raw)

    regulars.append({
        "id": user_id,
        "birth_date": birth_date.strftime("%d/%m/%Y"),
        "phone_num": phone_num,
        "identity": genere
    })

# Escriu els resultats a fitxers
with open("taula_user.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=usuaris[0].keys())
    writer.writeheader()
    writer.writerows(usuaris)

with open("taula_regular.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=regulars[0].keys())
    writer.writeheader()
    writer.writerows(regulars)

with open("taula_gender.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["identity"])
    for g in sorted(genders):
        writer.writerow([g])

print("Fitxers generats: taula_user.csv, taula_regular.csv i taula_gender.csv")
