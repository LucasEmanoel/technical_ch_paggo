docker stop $(docker ps -aq) && docker system prune -a && docker rm $(docker ps -aq) && docker rmi $(docker images -aq)
docker stop $(docker ps -aq) && docker rm technical_ch_paggo-api-service-1  && docker  rmi technical_ch_paggo_api-service
# Setup do projeto

## Ambiente Virtual Python

embora possa optar por utilizar o interpretador global, recomendo criar um venv para esse projeto.
basta simplesmente ir para a pasta raiz do projeto (`./technical_ch_paggo`) e rodar o seguinte comando :
`python3 -m venv .venv` 

1. python3 : interpretador do python
2. -m venv : modulo de criação de ambientes virtuais
3. .venv : pasta que será criada.

## Instalação de Dependencias


## Criação do banco de dados
Nessa etapa será realizada pelo docker, iremos configurar dois containers para rodar os dois bancos de dados em paralelo. 

 
## Referencias

- https://fastapi.tiangolo.com/deployment/docker/#check-it
- https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi
- https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/basic_use.html#defining-attributes