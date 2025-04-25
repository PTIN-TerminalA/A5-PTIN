import numpy as np
import random

# Generar datos de velocidad 
historial = []

def generar_velocidad():
    # Normalmente entre 40 y 60, con pequeñas variaciones
    return random.gauss(50, 3)  # media=50, desviación=3

def detectar_anomalia(historial, valor_actual, ventana_tamaño=10, lindar=20):
    if len(historial) < ventana_tamaño:
        return False  # No hay suficientes datos aún
    
    ventana = historial[-ventana_tamaño:]
    media = np.mean(ventana)
    desviacion = np.std(ventana)

    if abs(valor_actual - media) > lindar * desviacion:
        return True
    return False

# Simulación con 30 velocidades
for i in range(30):
    if i == 20:
        velocidad = 100  #ponemos un valor que debe ser anormal
    else:
        velocidad = generar_velocidad()
    
    es_anomalia = detectar_anomalia(historial, velocidad)

    historial.append(velocidad)

    if es_anomalia:
        estado = "Anomalia"  
    else:
        estado = "Normal"
    print(f"[{i+1}] Velocidad: {velocidad:.2f} km/h → {estado}")

