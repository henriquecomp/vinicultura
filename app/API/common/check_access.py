from fastapi import HTTPException
from application.services.security_service import decode_token


def check_access(token: str):
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
