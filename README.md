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

## Arquitetura e Tecnologias

**Tecnologias Principais**

* **FastAPI (Python):** Framework web para construção da API.
* **SQLAlchemy:** ORM para interação com o banco de dados.
* **Alembic:** Ferramenta para gerenciamento de migrações de esquema de banco de dados. O projeto inclui uma migração para criar a tabela de usuários (`4c4de80eabb5_create_user_table.py`).
* **JWT (JSON Web Tokens):** Para autenticação e autorização segura.
* **Web Scraping:** Utiliza bibliotecas como `requests` e `BeautifulSoup` (implícito pela funcionalidade e arquivos como `base_scrape.py`).
* **Pandas:** Para leitura e processamento dos arquivos CSV de fallback.
* **Docker e Docker Compose:** Para facilitar a configuração do ambiente e o deploy da aplicação.
* **Swagger UI:** Documentação da API gerada automaticamente e acessível via `/docs`.

## Estrutura do Projeto (Simplificada)

* **`app/api` (Camada de API):**
    * `controllers`: Definem os endpoints (rotas) da API (ex: `production_controller.py`).
    * `common/check_access.py`: Validação de token JWT.
* **`app/application` (Camada de Aplicação/Serviços):**
    * `services`: Contêm a lógica de negócio principal (ex: `production_service.py`).
    * Implementam o fallback para CSV em caso de falha no scraping.
    * `common/config.py`: Carrega configurações de URLs e arquivos CSV de fallback do `config.json`.
* **`app/domain` (Camada de Domínio):**
    * `entities`: Define as entidades de negócio (ex: `User`).
    * `enums`: Enumerações para categorias de produtos (ex: `ExportEnum`).
* **`app/infrastructure` (Camada de Infraestrutura):**
    * `db`: Configuração do banco de dados (SQLite).
    * `external_services`: Módulos de web scraping (ex: `production_scrape.py`).
    * `files`: Armazena os arquivos CSV de fallback (ex: `Producao.csv`, `Comercio.csv`).
    * `repositories`: Implementações concretas para acesso a dados (ex: `user_repository_sql.py`, `production_csv.py`).
* **`app/config.json`:** Arquivo central que armazena URLs para scraping e caminhos dos arquivos CSV.
* **`main.py`:** Ponto de entrada da aplicação FastAPI, configura middlewares de log.

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