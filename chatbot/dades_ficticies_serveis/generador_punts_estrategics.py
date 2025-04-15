import pandas as pd

# Paràmetres
tipus_punts = {
    'Lavabo': 15,
    'Àrea de Descans': 10,
    "Punt d'Informació": 5
}

ubicacions = [f"Terminal A - Porta {p}" for p in range(1, 30)]
horari = '00:00–24:00'

# Generació de punts
data_punts = []

for tipus, quantitat in tipus_punts.items():
    for i in range(1, quantitat + 1):
        nom = f"{tipus} {i}"
        ubicacio = ubicacions[(i - 1) % len(ubicacions)]
        data_punts.append([nom, tipus, ubicacio, horari])

# Exportació
df_punts = pd.DataFrame(data_punts, columns=['Nom', 'Tipus', 'Ubicació', 'Horari'])
df_punts.to_csv("punts_importants_aeroport.csv", index=False)

print(df_punts.head())
