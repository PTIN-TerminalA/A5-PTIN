Preparació de l'entorn
-----------------------

Requisit: Python >=3.10 i <3.13

Crea un entorn virtual: 
1- Instal·la el paquet python3.12-venv si no el tens instal·lat (permet crear entorns virtuals)

    sudo apt install python3.12-venv

2- Obre una terminal al directori dessitjat per crear l’entorn virtual (és important que es digui .venv)

    python3 -m venv .venv  # crea l'entorn virtual amb el nom venv

3- Un cop creat cal activar-lo (cada cop que sortiu quan torneu a entrar a la carpeta cal activar-ho de nou) amb la següent comanda:

    source .venv/bin/activate  # activa l'entorn virtual

Si funciona ara a la terminal t’ha de sortir (venv) abans del teu nom a la terminal.

Instal·la uv: 

    pip install uv
    # o, si falla (per linux):
    curl -LsSf https://astral.sh/uv/install.sh | sh 

Instal·la crewai: 

    uv tool install crewai

Instal·la dependències: 

    uv add langchain
    uv add ollama
    pip install 'crewai[tools]'
    #en cas que l’anterior doni error:
    pip install "crewai[tools]" 


Comprova que tens Ollama descarregat: ollama --version

Descarrega models amb Ollama:

    ollama pull llama3.1
    ollama pull mxbai-embed-large

!!sense acabar