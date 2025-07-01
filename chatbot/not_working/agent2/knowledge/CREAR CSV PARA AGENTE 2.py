import csv
import os

# Crea la carpeta si no existeix
os.makedirs("knowledge", exist_ok=True)

# Fitxer 1: rutes_transport.csv
rutes = [
    ["Terminal A", "Terminal B", 6, 15, "sí"],
    ["Terminal A", "Oficines", 4, 10, "sí"],
    ["Terminal B", "Oficines", 5, 12, "no"],
    ["Zona d'arribades", "Porta 12", 3, 8, "sí"],
    ["Zona comercial", "Terminal A", 2, 5, "sí"],
    ["Terminal B", "Zona d’arribades", 7, 16, "no"]
]

with open("knowledge/rutes_transport.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["origen", "destí", "temps_vehicle", "temps_peu", "vehicle_disponible"])
    writer.writerows(rutes)

# Fitxer 2: estacions.csv (llista d’estacions amb vehicles)
estacions = [
    ["Terminal A", "3", "sí"],
    ["Terminal B", "0", "no"],
    ["Zona d’arribades", "1", "sí"],
    ["Zona comercial", "2", "sí"]
]

with open("knowledge/estacions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ubicacio", "vehicles_disponibles", "activa"])
    writer.writerows(estacions)

# Fitxer 3: alternatives_transport.csv
alternatives = [
    ["Terminal A", "Terminal B", "vehicle autònom", "cinta transportadora"],
    ["Terminal B", "Oficines", "a peu", "vehicle autònom"],
    ["Zona comercial", "Terminal A", "vehicle autònom", "a peu"]
]

with open("knowledge/alternatives_transport.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["origen", "destí", "millor_opcio", "alternativa"])
    writer.writerows(alternatives)

print("Fitxers CSV creats a la carpeta 'knowledge/'")
