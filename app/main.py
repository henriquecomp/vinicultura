import logging
import time
import json
import uuid
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, Request, Response
from api.controllers.auth_controller import router as auth_controller
from api.controllers.production_controller import router as production_controller
from api.controllers.processing_controller import router as processing_controller
from api.controllers.commercialization_controller import (
    router as commercialization_controller,
)
from api.controllers.import_controller import router as import_controller
from api.controllers.export_controller import router as export_controller
from api.controllers.user_controller import router as user_controller


# Configuração do logging
log_file = f"app_{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    filename=log_file,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI()


def sanitize_body(body: Dict[str, Any]) -> Dict[str, Any]:
    """Substitui campos sensíveis (como 'password') por '***REDACTED***'."""
    sensitive_fields = {"password", "new_password", "senha", "token", "api_key", "authorization"}
    sanitized = body.copy()
    for field in sensitive_fields:
        if field in sanitized:
            sanitized[field] = "***REDACTED***"
    return sanitized


# Middleware para logar requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    guid = str(uuid.uuid4())[:8]  # Gera um GUID único para cada requisição]
    # Log da requisição recebida
    logger.info(f"ID: {guid} | Requisição recebida: {request.method} {request.url}")

    if request.method in ("POST", "PUT", "PATCH"):
        body = await request.body()

        try:
            # Converte bytes para JSON (se aplicável)
            body_json = json.loads(body.decode())
            sanitized_headers = sanitize_body(dict(request.headers))
            sanitized_body = sanitize_body(body_json)
            logger.info(f"ID: {guid} | Headers: {sanitized_headers}")
            logger.info(f"ID: {guid} | Request Body (JSON): {sanitized_body}")
        except json.JSONDecodeError:
            # Se não for JSON, loga como texto puro (limitado a 500 caracteres)
            logger.info(f"ID: {guid} | Request Body (Raw): {body.decode()[:500]}")

    # Processa a requisição e obtém a resposta
    response = await call_next(request)

    # Calcula o tempo de processamento
    process_time = time.time() - start_time
    process_time_ms = round(process_time * 1000, 2)  # Converte para milissegundos

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    # Reconstrói a resposta (pois o body_iterator foi consumido)
    response = Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )

    # Log da resposta
    logger.info(
        f"ID: {guid} | "
        f"Resposta enviada: {request.method} {request.url} | "
        f"Status: {response.status_code} | "
        f"Corpo Resposta: {response_body.decode()} | "
        f"Tempo: {process_time_ms}ms"
    )

    return response


app.include_router(auth_controller)
app.include_router(production_controller)
app.include_router(processing_controller)
app.include_router(commercialization_controller)
app.include_router(import_controller)
app.include_router(export_controller)
app.include_router(user_controller)
