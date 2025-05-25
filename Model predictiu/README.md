# API de Localització per RSSI

Aquesta API permet determinar la posició `(x, y)` d'un dispositiu basant-se en mesures RSSI de punts d’accés WiFi (BSSID). Utilitza un model de regressió entrenat i guardat com a `position_model.pkl`.

---

## Requisits

Instal·la les dependències amb:

```bash
pip install -r requirements.txt
````

## Execució del servidor

Per iniciar el servidor FastAPI:

```bash
uvicorn api:app --reload
```

> Assegura’t que el fitxer `position_model.pkl` es troba al mateix directori que el fitxer `api.py`.

---

## Endpoint disponible

### `POST /localize`

Envia un conjunt de mesures RSSI i obté una posició estimada.

#### Exemple de cos de la petició (`application/json`):

```json
{
  "measure": [
    { "bssid": "00:11:22:33:44:55", "rssi": -45.0 },
    { "bssid": "66:77:88:99:AA:BB", "rssi": -60.0 }
  ]
}
```

#### Resposta (`200 OK`):

```json
{
  "x": 0.4,
  "y": 0.1
}
```

#### Possibles errors:

* `500 Internal Server Error`: Si el model no està carregat o hi ha un error en la predicció.

---

## Exemple amb curl

```bash
curl -X POST http://127.0.0.1:8000/localize \
-H "Content-Type: application/json" \
-d '{
  "measure": [
    {"bssid": "00:11:22:33:44:55", "rssi": -40.0},
    {"bssid": "66:77:88:99:AA:BB", "rssi": -70.0}
  ]
}'
```

---

## Estructura del projecte

```
.
├── api.py                 # API FastAPI principal
├── predictiveModel.py      # Carrega i aplica el model
├── position_model.pkl      # Model de regressió serialitzat
├── requirements.txt        # Llista de dependències
└── README.md               # Documentació
```

---

## Notes addicionals

* El model `.pkl` s’ha de generar prèviament amb:

```python
joblib.dump((model, bssid_list), "position_model.pkl")
```
---