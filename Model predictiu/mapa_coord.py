
from PIL import Image, ImageDraw

#S'ha de instl·lar el paquet: pip install pillow


def marcar_punto_normalizado(ruta_imagen, x_norm, y_norm, salida='plano_marcado.png'):
    # Abrir la imagen
    imagen = Image.open("MapaTerminalA.png")
    ancho, alto = imagen.size

    # Convertir coordenadas normalizadas a píxeles
    x = int(x_norm * ancho)
    y = int(y_norm * alto)

    # Dibujar un círculo rojo en la posición calculada
    draw = ImageDraw.Draw(imagen)
    radio = 10
    draw.ellipse((x-radio, y-radio, x+radio, y+radio), fill='red')

    # Guardar imagen con marcador
    imagen.save(salida)
    print(f"Punto marcado en ({x_norm:.2f}, {y_norm:.2f}) y guardado como '{salida}'")


marcar_punto_normalizado("MapaTerminalA.png", 0.5, 0.5) 

