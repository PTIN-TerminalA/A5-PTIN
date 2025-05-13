# Pathfinding Cython Project

Este proyecto proporciona una implementación de Jump Point Search (JPS) optimizada en Cython, interoperable con una clase Python `GridMap` que convierte imágenes en mallas binarias. Incluye:

* Un script Python (`main.py`) que carga o define un grid, ejecuta la búsqueda y guarda/visualiza el resultado.

---

## Requisitos previos

* **Python 3.8+**
* **pip**
* **virtualenv** (recomendado)

---

## 1. Crear y activar un entorno virtual

> *Evita instalar librerías globalmente en tu sistema.*

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

## 2. Instalar dependencias

Con el entorno virtual activo, instala desde `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Estructura del proyecto (en caso de usar Cython)

```text
.
├── datastructure.py        # GridMap & imageToMatrix
├── main.py                 # Ejecutor de ejemplo & visualización
├── requirements.txt        # Dependencias Python
└── README.md               # Documentación (este fichero)
```

---

## 4. Ejecutar el ejemplo

```bash
python main.py
```

* Carga `map.png` (o la imagen que especifiques) via `imageToMatrix`.
* Ejecuta la búsqueda JPS desde `(0,0)` hasta `(height-1, width-1)`.
* Guarda la visualización en `PathAtoB.png`.

