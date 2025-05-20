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

## Production
@startuml
autonumber
actor Usuario
participant "ProductionController" as Controller
participant "CheckAccess" as CheckAccess
participant "ProductionService" as Application
participant "ApplicationConfig" as Config
participant "UrlHandler" as UrlHandler
participant "ProductionScrape" as Scrape
participant "BaseScrape" as BaseScrape

'Requisição autenticada
Usuario -> Controller: header: Authorization: Bearer token, get_production(year) 
Controller -> CheckAccess: check_access()

alt Token Válido
    alt 
        CheckAccess --> Controller: check_access()
        Controller -> Application: get_production_by_year(year)
        Application -> Config: get_config("Production") 
        Config --> Application: list[ConfigResponse]
        loop para cada item na lista de configuração
            Application -> UrlHandler: url_handler(url, year)
            UrlHandler --> Application: str (url)
            Application -> Scrape: get_production_by_year(url)
            Scrape -> BaseScrape: BaseScrape(url).handle()
            BaseScrape --> Scrape: list[BaseScrapeValueObject]
            Scrape --> Application: list[ProductionResponse]
        end
        Application --> Controller: list[ProductionResponse]
        Controller --> Usuario: 200 + list[ProductionResponse]
    else Exception
        Application --> Controller: Exception
        Controller --> Usuario: 500 + Internal Server Error { "detail": "message" }
else Token Inválido
    CheckAccess --> Controller: check_access(): Invalid token
    Controller --> Usuario: 401 Unauthorized

@enduml


## Commercialization

@startuml
autonumber
actor Usuario
participant "CommercializationController" as Controller
participant "CheckAccess" as CheckAccess
participant "CommercializationService" as Application
participant "ApplicationConfig" as Config
participant "UrlHandler" as UrlHandler
participant "CommercializationScrape" as Scrape
participant "BaseScrape" as BaseScrape

'Requisição autenticada
Usuario -> Controller: header: Authorization: Bearer token, get_commercialization(year) 
Controller -> CheckAccess: check_access()

alt Token Válido
    alt 
        CheckAccess --> Controller: check_access()
        Controller -> Application: get_commercialization_by_year(year)
        Application -> Config: get_config("Commercialization") 
        Config --> Application: list[ConfigResponse]
        loop para cada item na lista de configuração
            Application -> UrlHandler: url_handler(url, year)
            UrlHandler --> Application: str (url)
            Application -> Scrape: get_commercialization_by_year(url)
            Scrape -> BaseScrape: BaseScrape(url).handle()
            BaseScrape --> Scrape: list[BaseScrapeValueObject]
            Scrape --> Application: list[CommercializationResponse]
        end
        Application --> Controller: list[CommercializationResponse]
        Controller --> Usuario: 200 + list[CommercializationResponse]        
    else Exception
        Application --> Controller: Exception
        Controller --> Usuario: 500 + Internal Server Error { "detail": "message" }
else Token Inválido
    CheckAccess --> Controller: check_access(): Invalid token
    Controller --> Usuario: 401 Unauthorized

@enduml

## Processing

@startuml
autonumber
actor Usuario
participant "ProcessingController" as Controller
participant "CheckAccess" as CheckAccess
participant "ProcessingService" as Application
participant "ApplicationConfig" as Config
participant "UrlHandler" as UrlHandler
participant "ProcessingScrape" as Scrape
participant "BaseScrape" as BaseScrape

'Requisição autenticada
Usuario -> Controller: header: Authorization: Bearer token, get_processing(year) 
Controller -> CheckAccess: check_access()

alt Token Válido
    alt 
        CheckAccess --> Controller: check_access()
        Controller -> Application: get_processing_by_year(year)
        Application -> Config: get_config("Processing") 
        Config --> Application: list[ConfigResponse]
        loop para cada item na lista de configuração
            Application -> UrlHandler: url_handler(url, year)
            UrlHandler --> Application: str (url)
            Application -> Scrape: get_processing_by_year(url)
            Scrape -> BaseScrape: BaseScrape(url).handle()
            BaseScrape --> Scrape: list[BaseScrapeValueObject]
            Scrape --> Application: list[ProcessingResponse]
        end
        Application --> Controller: list[ProcessingResponse]
        Controller --> Usuario: 200 + list[ProcessingResponse]
    else Exception
        Application --> Controller: Exception
        Controller --> Usuario: 500 + Internal Server Error { "detail": "message" }
else Token Inválido
    CheckAccess --> Controller: check_access(): Invalid token
    Controller --> Usuario: 401 Unauthorized

@enduml

## Export

@startuml
autonumber
actor Usuario
participant "ExportController" as Controller
participant "CheckAccess" as CheckAccess
participant "ExportService" as Application
participant "ApplicationConfig" as Config
participant "UrlHandler" as UrlHandler
participant "ExportScrape" as Scrape
participant "BaseScrape" as BaseScrape

'Requisição autenticada
Usuario -> Controller: header: Authorization: Bearer token, get_export(year) 
Controller -> CheckAccess: check_access()

alt Token Válido
    alt 
        CheckAccess --> Controller: check_access()
        Controller -> Application: get_export_by_year(year)
        Application -> Config: get_config("Export") 
        Config --> Application: list[ConfigResponse]
        loop para cada item na lista de configuração
            Application -> UrlHandler: url_handler(url, year)
            UrlHandler --> Application: str (url)
            Application -> Scrape: get_export_by_year(url)
            Scrape -> BaseScrape: BaseScrape(url).handle()
            BaseScrape --> Scrape: list[BaseScrapeValueObject]
            Scrape --> Application: list[ExportResponse]
        end
        Application --> Controller: list[ExportResponse]
        Controller --> Usuario: 200 + list[ExportResponse]
    else Exception
        Application --> Controller: Exception
        Controller --> Usuario: 500 + Internal Server Error { "detail": "message" }
else Token Inválido
    CheckAccess --> Controller: check_access(): Invalid token
    Controller --> Usuario: 401 Unauthorized

@enduml


## Import

@startuml
autonumber
actor Usuario
participant "ImportController" as Controller
participant "CheckAccess" as CheckAccess
participant "ImportService" as Application
participant "ApplicationConfig" as Config
participant "UrlHandler" as UrlHandler
participant "ImportScrape" as Scrape
participant "BaseScrape" as BaseScrape

'Requisição autenticada
Usuario -> Controller: header: Authorization: Bearer token, get_import(year) 
Controller -> CheckAccess: check_access()

alt Token Válido
    alt 
        CheckAccess --> Controller: check_access()
        Controller -> Application: get_import_by_year(year)
        Application -> Config: get_config("Import") 
        Config --> Application: list[ConfigResponse]
        loop para cada item na lista de configuração
            Application -> UrlHandler: url_handler(url, year)
            UrlHandler --> Application: str (url)
            Application -> Scrape: get_import_by_year(url)
            Scrape -> BaseScrape: BaseScrape(url).handle()
            BaseScrape --> Scrape: list[BaseScrapeValueObject]
            Scrape --> Application: list[ImportResponse]
        end
        Application --> Controller: list[ImportResponse]
        Controller --> Usuario: 200 + list[ImportResponse]
    else Exception
        Application --> Controller: Exception
        Controller --> Usuario: 500 + Internal Server Error { "detail": "message" }
else Token Inválido
    CheckAccess --> Controller: check_access(): Invalid token
    Controller --> Usuario: 401 Unauthorized

@enduml
