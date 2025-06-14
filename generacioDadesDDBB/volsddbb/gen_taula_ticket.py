import csv
import random
from collections import defaultdict

# Carrega vols des del CSV
def carregar_vols(path='taula_flight.csv'):
    vols = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            vols.append(fila['id'])
    return vols

# Carrega usuaris regulars
def carregar_usuaris(path='idsregulars.txt'):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

# Genera número de seient únic
def generar_seient_ocupat(ocupats):
    files = list(range(1, 31))  # Files de 1 a 30
    lletres = list("ABCDEF")    # Seients A-F
    for fila in files:
        for lletra in lletres:
            seient = f"{fila}{lletra}"
            if seient not in ocupats:
                ocupats.add(seient)
                return seient
    return None

# Classe aleatòria
def classe_aleatoria():
    return random.choice(["economy", "premium economy", "business", "first"])

# Número de tiquet únic per usuari i vol
def generar_ticket_numero(flight_id, user_id):
    return f"TKT-{flight_id}-{user_id}"

# Enllaç QR fictici
def generar_qr(flight_id, user_id):
    return f"https://example.com/qr/{flight_id}/{user_id}"

# Genera la taula ticket assegurant que cada usuari té com a mínim un vol
def generar_taula_ticket_completa():
    vols = carregar_vols()
    usuaris = carregar_usuaris()
    tickets = []
    seients_ocupats_per_vol = defaultdict(set)

    for usuari in usuaris:
        random.shuffle(vols)
        ticket_afegit = False
        for vol in vols:
            seient = generar_seient_ocupat(seients_ocupats_per_vol[vol])
            if seient:
                ticket = {
                    'flight_id': vol,
                    'user_id': usuari,
                    'class': classe_aleatoria(),
                    'seat': seient,
                    'number': generar_ticket_numero(vol, usuari),
                    'qr_code_link': generar_qr(vol, usuari)
                }
                tickets.append(ticket)
                ticket_afegit = True
                break
        if not ticket_afegit:
            print(f"No s'ha pogut assignar cap vol al usuari {usuari}")
    return tickets

# Escriu el CSV de sortida
def escriure_csv(tickets, path='taula_ticket.csv'):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        camps = ['flight_id', 'user_id', 'class', 'seat', 'number', 'qr_code_link']
        writer = csv.DictWriter(f, fieldnames=camps)
        writer.writeheader()
        for ticket in tickets:
            writer.writerow(ticket)

# Executar
if __name__ == '__main__':
    tickets = generar_taula_ticket_completa()
    escriure_csv(tickets)
    print(f"S'han generat {len(tickets)} tiquets i s'han guardat a 'taula_ticket.csv'")
