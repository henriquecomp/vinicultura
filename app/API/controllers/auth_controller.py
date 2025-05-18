from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from infrastructure.db.database import get_db
from application.services.user_service import UserService

router = APIRouter()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Realiza o login do usuário

    Args:
        username (string): O e-mail do usuário cadastrado
        password (string): Senha do usuário cadastrado

    Returns:
        dict: Um dicionário seguindo a estrutura:
            {
                "access_token": str, # JWT Token da sessão
                "token_type": str, # Tipo do token "Bearer"
            }

    Raises:
        HTTPException: Se o usuário ou senha forem inválidos.
    """
    user = UserService().auth_by_email(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )

    return {"access_token": user.token, "token_type": "bearer"}
