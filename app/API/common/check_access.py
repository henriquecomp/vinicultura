from fastapi import HTTPException
from application.services.security_service import decode_token


def check_access(token: str):
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(token: str) -> str:
    payload = decode_token(token)
    username = payload.get("sub")
    if username is None:
        raise Exception(status_code=401, detail="Invalid token")
    return username
