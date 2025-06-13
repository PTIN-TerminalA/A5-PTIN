## Requisits

- Python 3.10 o superior
- FastAPI
- Uvicorn
- mysql-connector-python

Instal·lació de dependències:

```bash
pip install fastapi uvicorn mysql-connector-python
```

## Servidor

El servidor estarà disponible a:

```
http://10.60.0.3:4444
```

## Endpoint disponible

### `POST /recommendation`

Permet obtenir un servei recomanat basat en la ubicació i les preferències de l'usuari.

#### 🔸 Request body (JSON)

```json
{
  "x": 0.6460,
  "y": 0.1425,
  "id": 1425
}
```

#### 🔸 Resposta esperada

```json
{
  "recommendation": "Farmàcia 1"
}
```

Si no es troba cap servei recomanat:

```json
{
  "recommendation": null
}
```

## Estructura de fitxers

```
serviceRecommendation/
├── api.py                
├── recommendation.py     
└── README.md             
```