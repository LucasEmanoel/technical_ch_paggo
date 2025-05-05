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

4. Rodar o pipeline
```
dagster dev -f quickstart/assets.py
```

## Modelo
![Modelo](public/diagram.jpg "Modelo ER")
- Considerando bancos de dados em containers diferentes, é estabelecido uma relação logica entre data e sinal, apenas por timestamp.
- cada timestamp em sinal, será o primeiro valor dos registros agregados, o valor de agg_rows determina quantos registros de data devem ser utilizados na agregação: Ex: 10-Minutal irá utilizar 10 registros. 


## Refs
- https://docs.dagster.io/guides/build/partitions-and-backfills/partitioning-assets