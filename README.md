## Python Version

Deve ser utilizada a versão 3.13.2

## Criar o ambiente python

`python -m venv .venv`
`.venv\Scripts\activate`

## Instalar dependencias

Deve estar dentro do diretorio /path/to/app
`pip install -r /path/to/requirements.txt`

## Congelar dependências

Deve estar dentro do diretorio /path/to/app
`pip freeze > requirements.txt`

## Rodar a APP

Deve estar dentro do diretorio /path/to/app
`uvicorn main:app --reload`

## Alembic

Deve estar dentro do diretorio /path/to/app
`alembic revision --autogenerate -m "create user table"`
`alembic upgrade head`
