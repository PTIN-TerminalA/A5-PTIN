import sys
import csv

fitxerSortida = "resultats.txt"

def usage():
    print("Usage: python nomScript.py <data.csv>")

def checkLength():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    
    return sys.argv[1]

def readCSV(filename):
    fila = []

    try:
        with open(filename, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                i = {k: float(v) for k, v in row.items()}
                fila.append(i)

        return fila
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def classifyEstat(rows):
    lineas = []
    for idx, row in enumerate(rows):
        estat = evaluateEstat(
            row["entropia_ultrasonic"],
            row["temp_cpu"],
            row["cpu_percent"],
            row["ram_percent"],
            row["espai_sd_percent"],
            row["cam_variacio"]
        )

        lineas.append(f"--- Registre {idx} ---")
        lineas.append(f"Ultrasonic Sensor: {row['entropia_ultrasonic']} : {estat['entropia_ultrasonic']}")
        lineas.append(f"Rock4 Temperature: {row['temp_cpu']} : {estat['temp_cpu']}")
        lineas.append(f"CPU Usage: {row['cpu_percent']} : {estat['cpu_percent']}")
        lineas.append(f"RAM Memory: {row['ram_percent']} : {estat['ram_percent']}")
        lineas.append(f"SD Free Storage: {row['espai_sd_percent']} : {estat['espai_sd_percent']}")
        lineas.append(f"Camera Frame Deviation: {row['cam_variacio']} : {estat['cam_variacio']}")
        lineas.append("")
    return "\n".join(lineas)

def evaluateEstat(entropia, temp, cpu, ram, espai_sd, cam_variacio):
    statuses = {}

    if entropia < 0.5 or entropia > 20:
        statuses['entropia_ultrasonic'] = 'ERROR'
    else:
        statuses['entropia_ultrasonic'] = 'OK'

    if temp > 85:
        statuses['temp_cpu'] = 'ERROR'
    elif temp > 70:
        statuses['temp_cpu'] = 'WARNING'
    else:
        statuses['temp_cpu'] = 'OK'

    if cpu > 85:
        statuses['cpu_percent'] = 'WARNING'
    else:
        statuses['cpu_percent'] = 'OK'

    if ram > 95:
        statuses['ram_percent'] = 'ERROR'
    elif ram > 90:
        statuses['ram_percent'] = 'WARNING'
    else:
        statuses['ram_percent'] = 'OK'

    if espai_sd < 5:
        statuses['espai_sd_percent'] = 'ERROR'
    elif espai_sd < 15:
        statuses['espai_sd_percent'] = 'WARNING'
    else:
        statuses['espai_sd_percent'] = 'OK'

    if cam_variacio > 50:
        statuses['cam_variacio'] = 'ERROR'
    else:
        statuses['cam_variacio'] = 'OK'

    return statuses

def writeToFile(rows, fitxerSortida):
    try:
        with open(fitxerSortida, 'w') as out:
            out.write(classifyEstat(rows))
    except Exception as e:
        print(f"Error : {e}")
        sys.exit(1)

def revisaEstat(res):
    problema = [line for line in res.splitlines() if 'ERROR' in line or 'WARNING' in line]
    for problema in problema:
        alertaAdmin(problema)

def alertaAdmin(message):
    # Hauria que veure com enviar aquest missatge al admin del A3
    print(f"ALERTA ADMIN: {message}")

def main():
    filename = checkLength()
    rows = readCSV(filename)
    #writeToFile(rows, fitxerSortida)
    res = classifyEstat(rows)
    #print(res)
    revisaEstat(res)

if __name__ == "__main__":
    main()
