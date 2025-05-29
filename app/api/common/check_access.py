from fastapi import HTTPException
from app.application.services.security_service import decode_token


def check_access(token: str):
    """
        Dado um token, o valida se o token é valido

        Args:
            token (str): Token que o usuário recebeu durante o processo de autenticação

        Returns:

        
        Raises:
            HTTPException: Se o token é inválido
    """    
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(token: str) -> str:
    """
        Dado um token, recupera os dados do usuário no token (email)

        Args:
            token (str): Token que o usuário recebeu durante o processo de autenticação

        Returns:
            str: E-mail do usuário autenticado

        
        Raises:
            HTTPException: Se o token é inválido
    """        
    payload = decode_token(token)
    username = payload.get("sub")
    if username is None:
        raise Exception(status_code=401, detail="Invalid token")
    return username
