import mysql.connector
import argparse
import math

def calcular_distancia(x1, y1, x2, y2):
    """Calcula distancia euclidiana entre dos puntos"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def obtener_preferencias_usuario(cursor, user_id):
    """Obtiene las etiquetas de preferencia del usuario"""
    cursor.execute("SELECT pref FROM preferences WHERE id = %s", (user_id,))
    return [row[0] for row in cursor.fetchall()]

def obtener_servicios_recomendados(cursor, preferencias, user_x, user_y):
    """Obtiene servicios que coinciden con preferencias y están en radio"""
    query = """
        SELECT s.id, s.name, s.description, s.location_x, s.location_y 
        FROM service s
        JOIN service_tag st ON s.id = st.service_id
        WHERE st.tag_name IN (%s)
    """ % ','.join(['%s'] * len(preferencias))
    
    cursor.execute(query, tuple(preferencias))
    servicios = []
    
    for servicio in cursor.fetchall():
        serv_x = float(servicio[3])
        serv_y = float(servicio[4])
        distancia = calcular_distancia(user_x, user_y, serv_x, serv_y)
        
        if distancia <= 1.0:  # Ajusta este valor según tu escala
            servicios.append({
                'id': servicio[0],
                'nombre': servicio[1],
                'descripcion': servicio[2],
                'distancia': round(distancia * 100, 2),  # Asumiendo 1 unidad = 100 metros
                'coordenadas': (serv_x, serv_y)
            })
    
    return sorted(servicios, key=lambda x: x['distancia'])

def main():
    parser = argparse.ArgumentParser(description='Recomendador de servicios')
    parser.add_argument('--user-id', type=int, required=True, help='ID del usuario')
    parser.add_argument('--location-x', type=float, required=True, help='Coordenada X del usuario')
    parser.add_argument('--location-y', type=float, required=True, help='Coordenada Y del usuario')
    args = parser.parse_args()

    # Configuración de la conexión a la base de datos
    config = {
        'host': '192.168.10.10',
        'user': 'global',
        'password': 'Global_cloudA',
        'database': 'global'
    }

    try:
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()

        # Paso 1: Obtener preferencias del usuario
        preferencias = obtener_preferencias_usuario(cursor, args.user_id)
        
        if not preferencias:
            print("El usuario no tiene preferencias registradas.")
            return

        # Paso 2: Obtener servicios recomendados
        servicios = obtener_servicios_recomendados(cursor, preferencias, args.location_x, args.location_y)

        # Mostrar resultados
        print(f"\nRecomendaciones para el usuario {args.user_id}:")
        for servicio in servicios:
            print(f"\n• {servicio['nombre']}")
            print(f"  Descripción: {servicio['descripcion']}")
            print(f"  Distancia: {servicio['distancia']} metros")
            print(f"  Coordenadas: {servicio['coordenadas']}")

    except mysql.connector.Error as err:
        print(f"Error de base de datos: {err}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

if __name__ == "__main__":
    main()