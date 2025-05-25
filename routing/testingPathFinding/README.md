# API de Routing amb FastAPI

## Dependències

Assegura't de tenir instal·lades les següents dependències:
- FastAPI
- Uvicorn
- Pydantic
- NumPy
- Pillow

Pots instal·lar-les utilitzant pip:

```bash
pip install -r requirements.txt
```

## Execució de l'API

Per iniciar el servidor de desenvolupament:

```bash
uvicorn api:app --reload
```

Això posarà en marxa el servidor a `http://127.0.0.1:8000/`.

##  Documentació interactiva

FastAPI genera automàticament documentació interactiva a `http://127.0.0.1:8000/docs

##  Endpoint principal

### POST /path

Calcula el camí més curt entre dos punts en el mapa.

#### Cos de la sol·licitud

Espera un JSON amb les coordenades normalitzades dels punts d'inici i final:

```json
{
  "start": [x_start, y_start],
  "goal": [x_goal, y_goal]
}
```
- `start`: Coordenades normalitzades del punt d'inici (valors entre 0 i 1).
- `goal`: Coordenades normalitzades del punt de destí (valors entre 0 i 1).

#### Exemple de sol·licitud amb curl

```bash
curl -X POST "http://127.0.0.1:8000/path" \
  -H "Content-Type: application/json" \
  -d '{
    "start": [0.5015634772, 0.3986866792],
    "goal": [0.5109443402, 0.3367729831]
  }'
```

#### Resposta esperada

Si es troba un camí, la resposta serà un JSON amb:
- `length`: Nombre total de passos en el camí.
- `path`: Llista de punts del camí, cadascun amb coordenades normalitzades.

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

#### Codis d'error

- `400 Bad Request`: Si els punts estan fora dels límits del mapa o no són transitables.
- `404 Not Found`: Si no es pot trobar cap camí entre els punts especificats.

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

