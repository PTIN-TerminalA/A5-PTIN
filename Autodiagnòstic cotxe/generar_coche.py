import random
import csv

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

        writer.writerow({
            "entropia_ultrasonic": round(entropia, 2),
            "temp_cpu": round(temp, 1),
            "cpu_percent": round(cpu, 1),
            "ram_percent": round(ram, 1),
            "espai_sd_percent": round(espai_sd, 1),
            "cam_variacio": round(cam_var, 2),
        })
