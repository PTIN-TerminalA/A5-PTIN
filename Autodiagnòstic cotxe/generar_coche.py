import random
import csv

def classifica_estat(entropia, temp, cpu, ram, espai_sd, cam_variacio):
    errors = []
    precaucions = []

    if entropia < 0.5 or entropia > 20:
        errors.append("ULTRASONIC")

    if temp > 85:
        errors.append("TEMP")
    elif temp > 70:
        precaucions.append("TEMP")

    if cpu > 85:
        precaucions.append("CPU")

    if ram > 95:
        errors.append("RAM")
    elif ram > 90:
        precaucions.append("RAM")

    if espai_sd < 5:
        errors.append("SD")
    elif espai_sd < 15:
        precaucions.append("SD")

    if cam_variacio > 50:
        errors.append("CAM")

    if errors:
        return "ERROR_" + "_".join(errors)
    elif precaucions:
        return "PRECAUCIO_" + "_".join(precaucions)
    else:
        return "OK"

# Generar dataset
with open("dades_sintetiques.csv", "w", newline="") as f:
    fieldnames = ["entropia_ultrasonic", "temp_cpu", "cpu_percent", "ram_percent", "espai_sd_percent", "cam_variacio"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for _ in range(1000):
        entropia = random.uniform(0, 25)
        temp = random.uniform(40, 95)
        cpu = random.uniform(10, 100)
        ram = random.uniform(20, 100)
        espai_sd = random.uniform(0, 100)
        cam_var = random.uniform(0, 70)

        #estat = classifica_estat(entropia, temp, cpu, ram, espai_sd, cam_var)

        writer.writerow({
            "entropia_ultrasonic": round(entropia, 2),
            "temp_cpu": round(temp, 1),
            "cpu_percent": round(cpu, 1),
            "ram_percent": round(ram, 1),
            "espai_sd_percent": round(espai_sd, 1),
            "cam_variacio": round(cam_var, 2),
            #"estat": estat
        })
