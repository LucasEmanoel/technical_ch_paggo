- docker stop $(docker ps -aq) && docker system prune -a && docker rm $(docker ps -aq) && docker rmi $(docker images -aq)

# Setup do projeto
## Pré requisitos
1. Python e Pip instalados
2. Docker e Compose instalados
## Etapas
1. Na raiz do projeto (`./technical_ch_paggo`) criar e ativar um ambiente virtual:
```python3
python3 -m venv .venv
```
- linux/mac
```
source .venv/bin/activate
```
- Windows
```
source venv\Scripts\activate
```

2. Instalar dependencias:
```
pip install -r api/requirements.txt
```
3. Rodar aplicação FastApi, considerando que já tenha o docker + [compose](https://github.com/docker/compose)
```
docker-compose up --build
```
 
## Modelo


