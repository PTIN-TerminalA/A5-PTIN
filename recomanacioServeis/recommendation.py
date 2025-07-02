import math
import mysql.connector
from mysql.connector import Error

def dist(x1, y1, x2, y2):
    return math.sqrt((float(x2) - float(x1))**2 + (float(y2) - float(y1))**2)

def getPref(cursor, uID):
    cursor.execute("SELECT pref FROM preferences WHERE id = %s", (uID,))
    return [row[0] for row in cursor.fetchall()]

'''
def normalizeCoord(xNorm: float, yNorm: float, height: int, width: int) -> Tuple[int, int]:
    j = int(round((width - 1) * xNorm))
    i = int(round((height - 1) * (1 - yNorm)))
    return (i, j)
'''

def getRecommendedServices(cursor, pref, x, y):
    query = """
        SELECT s.id, s.name, s.location_x, s.location_y 
        FROM service s
        JOIN service_tag st ON s.id = st.service_id
        WHERE st.tag_name IN (%s)
    """ % ','.join(['%s'] * len(pref))

    cursor.execute(query, tuple(pref))
    services = []

    for s in cursor.fetchall():
        serviceX = s[2]
        serviceY = s[3]

        '''
        pServei = normalizeCoord(serviceX, serviceY, altura, amplada) 
        pUser = normalizeCoord(x, y, altura, amplada)
        ''' 

        distance = dist(x, y, serviceX, serviceY)

        if distance <= 0.2:
            services.append({
                'id': s[0],
                'name': s[1],
                'dist': distance,
                'pos': (serviceX, serviceY)
            })

    sortedServices = sorted(services, key=lambda x: x['dist'])
    return [service['name'] for service in sortedServices]

def connect(x, y, userID):
    try:
        conn = mysql.connector.connect(
            host='192.168.10.10',
            user='global',
            password='Global_cloudA',
            database='global'
        )
        cursor = conn.cursor()

        pref = getPref(cursor, userID)
        services = getRecommendedServices(cursor, pref, x, y)
        cursor.close()
        conn.close()

        # De moment, només un servei
        return services[0] if services else None
    except Error as err:
        return None
    
def kickoff(x, y, userID):
    service = connect(x, y, userID)
    return service
