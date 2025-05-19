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
`uvicorn main:app --reload --log-level debug`

## Alembic

Deve estar dentro do diretorio /path/to/app
`alembic revision --autogenerate -m "create user table"`
`alembic upgrade head`

## Próximos passos

- Tirar as urls e colocar em um arquivo de configuração (Henrique) - OK
- Ler os arquivos csvs e transformar em resposta em caso de falha da url (Eliel)
- Deixar a aplicação resiliente com try catch (Eliel)
- Cadastro de usuário (Henrique) - OK
- JWT Token e fechar as rotas (Henrique) - OK
- Alterar senha do usuário desde que ele esteja logado. - OK
- Logs (Henrique) - OK
- Testes unitários (Henrique e Eliel)
- Deploy na nuvem (Henrique e Eliel)
- Documentar os métodos com DocString (Henrique e Eliel)
- Criar o diagrama de arquitetura (Henrique e Eliel)
- Video de apresentacao (Henrique e Eliel)
- Documentar no README conforme solicitação da FIAP (Henrique e Eliel)


# Diagrama de Sequencia
Use o editor https://editor.plantuml.com/ para visual o diagrama.

## Criação de usuário
@startuml
autonumber
actor Usuario
participant "UserController" as Controller
participant "CheckAccess" as CheckAccess
participant "UserService" as Application
participant "UserRepository" as Repository

'Requisição autenticada
Usuario -> Controller: Authorization: Bearer token
Controller -> CheckAccess: check_access()

alt Token Válido
    CheckAccess -> Controller: check_access()
    Controller -> Application: add_user(db, username, email, password)
    Application -> Repository: save(user)
    Repository --> Application: User
    Application --> Controller: UserResponse
    Controller --> Usuario: 200 + UserResponse
else Token Inválido
    CheckAccess --> Controller: check_access(): Invalid token
    Controller --> Usuario: 401 Unauthorized

@enduml

## Change Password
@startuml
autonumber
actor Usuario
participant "UserController" as Controller
participant "CheckAccess" as CheckAccess
participant "UserService" as Application
participant "UserRepository" as Repository

'Requisição autenticada
Usuario -> Controller: Authorization: Bearer token
Controller -> CheckAccess: check_access()

alt Token Válido
    CheckAccess -> Controller: check_access()
    alt Success
        Controller -> Application: change_password(db, current_user_email, newpassword)
        Application -> Repository: update(user)
        Repository --> Application: User
        Application --> Controller: UserResponse
        Controller --> Usuario: 200 + UserResponse
    else Exception
        Application --> Controller: raise_exception
        Controller --> Usuario: 500 Internal Server Error
else TokenInvalid
    CheckAccess --> Controller: check_access(): Invalid token
    Controller --> Usuario: 401 Unauthorized

@enduml


## Auth

@startuml
autonumber
actor Usuario
participant "AuthController" as Controller
participant "UserService" as Application
participant "UserRepository" as Repository

'Requisição autenticada

alt ValidUser
    Usuario -> Controller: login(username, password)
    Controller -> Application: auth_by_email(db, username, password)
    Application -> Repository: get_by_email(email)
    Repository --> Application: User
    Application --> Application: _check_password(password, userPassword)
    Application --> Application: create_access_token(email)
    Application --> Controller: AuthResponse
    Controller --> Usuario: 200 + { "access_token" + "token_type" }
else InvalidUser
    Application --> Controller: check_password(): None
    Controller --> Usuario: 401 Unauthorized

@enduml