# Agent3 Crew

Benvingut al projecte Agent3 Crew, impulsat per crewAI. Aquesta plantilla està dissenyada per ajudar-te a configurar un sistema d’IA multiagent de manera senzilla, aprofitant el potent i flexible marc que proporciona crewAI. El nostre objectiu és permetre que els teus agents col·laborin de manera efectiva en tasques complexes, maximitzant la seva intel·ligència col·lectiva i les seves capacitats.

## Instal·lació

Assegura't de tenir instal·lat Python >=3.10 i <3.13 al teu sistema. Aquest projecte utilitza UV per a la gestió de dependències i paquets, oferint una experiència d’instal·lació i execució fluïda.

### Crewai
Primer, si encara no ho tenim fet, instal·lem uv:

```bash
pip install uv
```
O si no també es pot instal·lar uv amb:

Linux 
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Windows
```bash 
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

A continuació, ves al directori del teu projecte i instal·la les dependències:

Instal·lem primer crewai:

```bash
uv tool install crewai
```

Un cop instal·lat hem d'instal·lar les dependències:

```bash
uv add langchain
uv add ollama
pip install 'crewai[tools]' , si dona error: pip install "crewai[tools]"

```
### Personalització

- Mofica `src/agent3/config/agents.yaml` per a definir els agents
- Modifica `src/agent3/config/tasks.yaml` per a definir les tasques 
- Modifica `src/agent3/crew.py` per afegir la teva pròpia lògica, eines i arguments específics
- Modifica `src/agent3/main.py` per afegir entrades personalitzades per als teus agents i tasques

### Ollama
En tindre tot el necessari per a crewai, ens quedaria descarregar el model de ollama que farem servir i també el embbeder. 
Per fer tot això, se suposa que ja tenim el programa ollama instal·lat. 

Instal·lem el model pre-entrenat
```bash
ollama pull llama3.1
```

Instal·lem el embbeder 
```bash
ollama pull mxbai-embed-large
```

## Executar el projecte

Per posar en marxa el teu equip d’agents d’IA i començar l’execució de tasques, executa això des de la carpeta arrel del teu projecte:

```bash
$ crewai run
```
Aquesta comanda inicialitza l’equip Agent3, agrupant els agents i assignant-los les tasques segons la configuració definida.




