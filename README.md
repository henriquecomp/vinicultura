# Vinicultura
Este é um projeto desenvolvido em FastAPI, que inclui web scraping do site http://vitibrasil.cnpuv.embrapa.br/. Em caso de falha no web scraping ele irá ler um arquivo com os dados que são disponibilizados para download. Só é possível realizar o scrape/ler os arquivos usuários que estão autenticados através de JWT Token válido.

## Funcionalidades
- Autenticação através de JWT Token (/login)
- Web scraping de dados de produção (/production)
- Web scraping de dados de processamento (/processing)
- Web scraping de dados de comercialização (/commercialization)
- Web scraping de dados de importação (/import)
- Web scraping de dados de exportação (/export)
- Fallback para CSV em caso de erro do site da embrapa
- Cadastro de usuário (/users)
- Alteração de senha do usuário autenticado (/change-password)
- Logs requisições de entrada e saída da aplicação


## Estrutura do Projeto
```bash
vinicultura
├── app
│   ├── alembic
│   │   ├── env.py
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── 4c4de80eabb5_create_user_table.py
│   ├── alembic.ini
│   ├── api
│   │   ├── common
│   │   │   └── check_access.py
│   │   ├── controllers
│   │   │   ├── auth_controller.py
│   │   │   ├── commercialization_controller.py
│   │   │   ├── export_controller.py
│   │   │   ├── import_controller.py
│   │   │   ├── processing_controller.py
│   │   │   ├── production_controller.py
│   │   │   └── user_controller.py
│   │   └── models
│   │       └── requests
│   │           ├── user_change_password_request.py
│   │           └── user_create_request.py
│   ├── application
│   │   ├── common
│   │   │   ├── config.py
│   │   │   └── url_handler.py
│   │   ├── DTOs
│   │   │   ├── auth_response.py
│   │   │   ├── commercialization_response.py
│   │   │   ├── config_response.py
│   │   │   ├── export_response.py
│   │   │   ├── import_response.py
│   │   │   ├── processing_response.py
│   │   │   ├── production_response.py
│   │   │   └── user_response.py
│   │   └── services
│   │       ├── commercialization_service.py
│   │       ├── export_service.py
│   │       ├── import_service.py
│   │       ├── processing_service.py
│   │       ├── production_service.py
│   │       ├── security_service.py
│   │       └── user_service.py
│   ├── architecture_diagrams
│   │   ├── sequence_endpoint_commercialization.png
│   │   ├── sequence_endpoint_commercialization.txt
│   │   ├── sequence_endpoint_export.png
│   │   ├── sequence_endpoint_export.txt
│   │   ├── sequence_endpoint_import.png
│   │   ├── sequence_endpoint_import.txt
│   │   ├── sequence_endpoint_processing.png
│   │   ├── sequence_endpoint_processing.txt
│   │   ├── sequence_endpoint_production.png
│   │   ├── sequence_endpoint_production.txt
│   │   ├── sequence_endpoint_user_authentication.png
│   │   ├── sequence_endpoint_user_authentication.txt
│   │   ├── sequence_endpoint_user_change_password.png
│   │   ├── sequence_endpoint_user_change_password.txt
│   │   ├── sequence_endpoint_user_create.png
│   │   └── sequence_endpoint_user_create.txt
│   ├── config.json
│   ├── domain
│   │   ├── entities
│   │   │   └── user.py
│   │   ├── enums
│   │   │   ├── export_enum.py
│   │   │   ├── import_enum.py
│   │   │   └── processing_enum.py
│   │   ├── repositories
│   │   │   └── user_repository.py
│   │   └── value_objects
│   │       └── base_scrape.py
│   └── infrastructure
│       ├── db
│       │   ├── app.sqlite3
│       │   └── database.py
│       ├── external_services
│       │   ├── base_scrape.py
│       │   ├── commercialization_scrape.py
│       │   ├── export_scrape.py
│       │   ├── import_scrape.py
│       │   ├── processing_scrape.py
│       │   └── production_scrape.py
│       ├── files
│       │   ├── Comercio.csv
│       │   ├── ExpEspumantes.csv
│       │   ├── ExpSuco.csv
│       │   ├── ExpUva.csv
│       │   ├── ExpVinho.csv
│       │   ├── ImpEspumantes.csv
│       │   ├── ImpFrescas.csv
│       │   ├── ImpPassas.csv
│       │   ├── ImpSuco.csv
│       │   ├── ImpVinhos.csv
│       │   ├── ProcessaAmericanas.csv
│       │   ├── ProcessaMesa.csv
│       │   ├── ProcessaSemclass.csv
│       │   ├── ProcessaViniferas.csv
│       │   └── Producao.csv
│       └── repositories
│           ├── commercialization_csv.py
│           ├── export_csv.py
│           ├── import_csv.py
│           ├── processing_csv.py
│           ├── production_csv.py
│           └── user_repository_sql.py
├── docker-compose.yml
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt
└── tests
    ├── __init__.py
    ├── controllers
    │   ├── __init__.py
    │   └── test_production_service.py
    ├── infrastructure
    │   └── external_services
    │       ├── test_base_scrape.py
    │       └── test_production_scrape.py
    └── services
        └── test_production_service_scrape.py
```

 - **`app/`** Esta é a pasta raiz da aplicação FastAPI. Ela contém toda a lógica e os componentes necessários para o funcionamento do sistema.
-   **`app/API/`**: Responsável pela camada de Interface de Programação de Aplicações (API).
    -   **`app/API/common/`**: Contém módulos utilitários comuns para a camada de API, como o `check_access.py`, que lida com a validação de tokens de acesso.
    -   **`app/API/controllers/`**: Define os endpoints da API (rotas). Cada arquivo aqui (ex: `auth_controller.py`, `production_controller.py`) gerencia as requisições HTTP para um recurso específico, validando entradas, chamando os serviços apropriados da camada de aplicação e formatando as respostas.
    -   **`app/API/models/`**: Contém os modelos de dados Pydantic usados para validar os corpos das requisições e, possivelmente, formatar respostas.
        -   **`app/API/models/requests/`**: Especificamente, define os modelos para os dados esperados nas requisições (ex: `user_create_request.py`, `user_change_password_request.py`).
-   **`app/alembic/`**: Configuração e scripts para o Alembic, uma ferramenta de migração de banco de dados para SQLAlchemy.
    
    -   **`app/alembic/versions/`**: Armazena os arquivos de script de migração gerados pelo Alembic, que descrevem as alterações no esquema do banco de dados ao longo do tempo (ex: `4c4de80eabb5_create_user_table.py` que cria a tabela de usuários).
    -   `alembic.ini` e `env.py` são arquivos de configuração do Alembic.
    
-   **`app/application/`**: Representa a camada de lógica de aplicação (ou camada de serviço). Ela orquestra as interações entre a camada de API e a camada de domínio/infraestrutura.
    
    -   **`app/application/common/`**: Módulos utilitários para a camada de aplicação, como `config.py` para carregar configurações de URLs e arquivos CSV de fallback, e `url_handler.py` para manipular URLs usadas na raspagem de dados.
   
    -   **`app/application/DTOs/`**: Contém os Data Transfer Objects (DTOs). São classes simples usadas para transferir dados entre camadas, especialmente para formatar respostas dos serviços para os controllers (ex: `production_response.py`, `user_response.py`).
    
    -   **`app/application/services/`**: Contém a lógica de negócio principal da aplicação. Os serviços (ex: `production_service.py`, `user_service.py`) são responsáveis por executar as tarefas solicitadas pelos controllers, interagir com repositórios e outros serviços. Eles também implementam a lógica de fallback para ler arquivos CSV em caso de falha na raspagem de dados.
    
- **`architecture_diagrams`**: Contém os diagramas de sequencia  dos endpoints da aplicação. 	     
	- Os arquivos .txt podem ser modificados no site https://editor.plantuml.com/  
	- Os arquivos .png são gerados a partir dos arquivos .txt no site https://editor.plantuml.com/ e realizado o download da imagem para melhor compreensão.
    
-   **`app/domain/`**: Contém a lógica de domínio da aplicação, representando as entidades de negócio, regras e objetos de valor.
    
    -   **`app/domain/entities/`**: Define as entidades principais do domínio, como a classe `User` que mapeia para a tabela de usuários no banco de dados.
    
    -   **`app/domain/enums/`**: Define enumerações usadas no domínio para representar conjuntos fixos de valores (ex: `ExportEnum`, `ProcessingEnum`).
    
    -   **`app/domain/repositories/`**: Define as interfaces (contratos) para os repositórios de dados (ex: `UserRepository`). Estas interfaces abstraem a forma como os dados são persistidos ou recuperados.
    
    -   **`app/domain/value_objects/`**: Contém objetos de valor, que são pequenos objetos representando conceitos simples do domínio (ex: `BaseScrapeValueObject` para padronizar o retorno da raspagem de dados).
    
-   **`app/infrastructure/`**: Responsável pelos detalhes de implementação técnica, como acesso a banco de dados, serviços externos e arquivos.
    
    -   **`app/infrastructure/db/`**: Configuração e código relacionado ao banco de dados, como `database.py` que configura a engine SQLAlchemy e a sessão do banco de dados.
    
    -   **`app/infrastructure/external_services/`**: Módulos para interagir com serviços externos, principalmente para a raspagem de dados de sites da Embrapa (ex: `base_scrape.py`, `production_scrape.py`).
    
    -   **`app/infrastructure/files/`**: Armazena os arquivos CSV que servem como fonte de dados de fallback caso a raspagem de dados dos sites da Embrapa falhe (ex: `Comercio.csv`, `Producao.csv`).
  
    -   **`app/infrastructure/repositories/`**: Implementações concretas das interfaces de repositório definidas na camada de domínio. Por exemplo, `user_repository_sql.py` implementa o acesso aos dados do usuário usando SQLAlchemy, enquanto outros arquivos (ex: `production_csv.py`) implementam a leitura dos arquivos CSV de fallback.
   
-   `app/config.json`: Arquivo de configuração central que armazena URLs para raspagem de dados e os caminhos para os arquivos CSV de fallback correspondentes a cada tipo de dado (Produção, Processamento, etc.).
    
- **`tests/`** Esta pasta contém os testes automatizados para a aplicação, garantindo a qualidade e o correto funcionamento do código.

-   **`tests/controllers/`**: Testes para os controllers da API, verificando se as rotas se comportam como esperado, se chamam os serviços corretamente e retornam as respostas adequadas (ex: `test_production_service.py`, embora o nome sugira teste de serviço, ele testa o _controller_ `production_controller`).

-   **`tests/infrastructure/`**: Testes para os componentes da camada de infraestrutura.
-
    -   **`tests/infrastructure/external_services/`**: Testes específicos para os serviços de raspagem de dados (ex: `test_base_scrape.py`, `test_production_scrape.py`), verificando se eles extraem e processam os dados corretamente das fontes externas (mockadas durante o teste).
    
-   **`tests/services/`**: Testes para a lógica de negócio na camada de aplicação (serviços), verificando se as regras de negócio são aplicadas corretamente e se a interação com outras camadas (como repositórios e scrapers, geralmente mockados) funciona como esperado (ex: `test_production_service_scrape.py`).

-   `README.md`: Fornece informações sobre o projeto, como configuração do ambiente, instalação de dependências, como rodar a aplicação e os próximos passos do desenvolvimento.

-   `docker-compose.yml`: Define os serviços, redes e volumes para rodar a aplicação em containers Docker, facilitando o deploy e a configuração do ambiente.

-   `main.py`: Ponto de entrada da aplicação FastAPI. Ele inicializa a aplicação, inclui os routers dos controllers e pode configurar middlewares (como o de logging de requisições implementado).
-
-   `requirements.txt`: Lista todas as dependências Python do projeto com suas versões específicas, permitindo a recriação do ambiente de forma consistente.

## Pré Requisitos

- Deve ser utilizada a versão 3.13.2
- Deve ter o Docker Desktop instalado caso queira executar via Docker

## Executar o projeto

**1. Clone o repositório**
`git clone https://github.com/henriquecomp/vinicultura.git` 
`cd vinicultura`

**2. Crie um ambiente virtual**
`python -m venv .venv`
`source .venv/bin/activate (macOS e Linux)`
`.venv\Scripts\activate (Windows)`

**3. Instale as dependências**
`pip install -r requirements.txt`

Caso instale/adicione uma nova dependência no projeto, atualize o arquivo requirements.txt
`pip freeze > requirements.txt`

**4. Crie o arquivo .env na raiz do projeto**
```bash
SECRET_KEY="sua-chave-secreta-aqui"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**5. Execute o aplicativo**
`uvicorn main:app --reload`
  
**6. Criando uma migration**
Deve estar dentro do diretorio /path/to/app
`alembic revision --autogenerate -m "create user table"`
`alembic upgrade head`

## Executar projeto com Docker
```
docker build -t vinicultura .
docker run -p 8000:8000 vinicultura
```

## Documentação da API
A documentação da API é gerada automaticamente com Swagger e está disponível em `http://127.0.0.1:8000/docs/`  


## URL de demonstração
https://vinicultura.onrender.com/docs