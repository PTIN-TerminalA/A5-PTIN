import json
import qrcode # pip install qrcode[pil]
import os

def generate_qr_from_json(json_path, output_path):
    # Llegeix el fitxer JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Converteix a string JSON (compacte)
    json_string = json.dumps(data, separators=(",", ":"))

    # Genera el codi QR
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(json_string)
    qr.make(fit=True)

    # Renderitza la imatge QR
    img = qr.make_image(fill_color="black", back_color="white")

    # Desa la imatge
    img.save(output_path)
    print(f"QR generat a: {output_path}")


# Genera tants QRs com jsons hi ha a la carpeta input
if __name__ == "__main__":
    input_folder = "boarding_passes_qr_json"
    output_folder = "generated_qrs"

    # Crea la carpeta de sortida si no existeix
    os.makedirs(output_folder, exist_ok=True)

    # Processa tots els fitxers .json dins la carpeta
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            json_path = os.path.join(input_folder, filename)
            output_filename = filename.replace(".json", "_qr.png")
            output_path = os.path.join(output_folder, output_filename)

            generate_qr_from_json(json_path, output_path)


# Genera 1 QR
#if __name__ == "__main__":
    # Ruta al fitxer JSON
#    input_json = "boarding_passes_qr_json/boarding_pass_1.json"  # Canvia-ho pel teu fitxer
#    output_qr = "boarding_pass_1_qr.png"    # Nom del fitxer de sortida

#    generate_qr_from_json(input_json, output_qr)