## API de Routing amb FastAPI

## Dependències

Assegura't de tenir instal·lades les següents dependències:

* fastapi
* uvicorn
* pydantic
* numpy
* pillow

Pots instal·lar-les amb:

```bash
pip install -r requirements.txt
```

---

## Execució de l'API

Pots arrencar el servidor de dues maneres:

1. **Directament amb uvicorn (CLI):**

```bash
uvicorn api:app --reload
```

2. **Executant el script Python:**

```bash
python3 api.py
```

En ambdós casos el servei estarà disponible a `http://127.0.0.1:5000/`. A no ser que modifiquem el host o el port en la funció main de api.py

## Documentació interactiva

## Endpoints

### POST /path

Calcula el camí més curt entre dos punts dins del mapa.

#### Cos de la sol·licitud

```json
{
  "start": [x_start, y_start],
  "goal":  [x_goal,  y_goal]
}
```

* `start`: Coordenades normalitzades del punt d'inici (valors entre 0 i 1).
* `goal`:  Coordenades normalitzades del punt de destí (valors entre 0 i 1).

#### Exemple amb **curl**

```bash
curl -X POST "http://127.0.0.1:5000/path" \
  -H "Content-Type: application/json" \
  -d '{
    "start": [0.5016, 0.3987],
    "goal":  [0.5109, 0.3368]
  }'
```

#### Resposta exitosa

```json
{
  "length": 273,
  "path": [
    [0.501, 0.398],
    [0.502, 0.397],
    ...
  ]
}
```

* `length`: Nombre de punts (waypoints) del camí simplificat.
* `path`:  Llista de coordenades normalitzades de cada punt del camí.

#### Codis d'error

* **400 Bad Request**: Punt d'inici o destí fora del mapa o ocupat per un obstacle.
* **404 Not Found**: No s'ha pogut trobar cap ruta.

---

### POST /getNearest

Troba el servei més proper respecte a una posició d'usuari i retorna el seu **id**.

#### Cos de la sol·licitud

```json
{
  "position": [x_user, y_user],
  "request": {
    "<id>": [x_serv, y_serv],
    "...":       [x_serv, y_serv],
    ...
  }
}
```

* `position`: Coordenades normalitzades (0–1) de l'usuari.
* `request`: Diccionari amb clau `id` (integer) i valor `[x, y]` normalitzat.

#### Exemple amb **curl**

```bash
curl -X POST "http://127.0.0.1:5000/getNearest" \
  -H "Content-Type: application/json" \
  -d '{
    "position": [0.45, 0.30],
    "request": {
      "101": [0.20, 0.75],
      "102": [0.80, 0.10],
      "103": [0.50, 0.50]
    }
  }'
```

#### Resposta exitosa

```json
{
  "id": 102
}
```

* `id`: Identificador (clau) del servei més proper accessible.

#### Codis d'error

* **400 Bad Request**: La posició d'origen està fora del mapa o ocupada per un obstacle.
* **404 Not Found**: Cap servei accessible des de la posició donada.

---

## Estructura del projecte

```
project/
├── api.py
├── datastructure.py
├── pathfinding.py
├── TerminalA.jpg
├── requirements.txt
└── README.md
```
