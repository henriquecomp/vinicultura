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

## Próximos passos

- Tirar as urls e colocar em um arquivo de configuração (Henrique)
- Ler os arquivos csvs e transformar em resposta em caso de falha da url (Eliel)
- Deixar a aplicação resiliente com try catch (Eliel)
- Cadastro de usuário (Henrique)
- JWT Token e fechar as rotas (Henrique)
- Logs (Henrique)
- Testes unitários (Henrique e Eliel)
- Deploy na nuvem (Henrique e Eliel)
- Documentar os métodos com DocString (Henrique e Eliel)
- Criar o diagrama de arquitetura (Henrique e Eliel)
- Video de apresentacao (Henrique e Eliel)
- Documentar no README conforme solicitação da FIAP (Henrique e Eliel)
