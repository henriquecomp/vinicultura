from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.application.DTOs.user_response import UserResponse
from app.api.models.requests.user_create_request import UserCreateRequest
from app.api.models.requests.user_change_password_request import UserChangePasswordRequest
from app.application.services.user_service import UserService
from app.infrastructure.db.database import get_db
from app.api.common.check_access import check_access, get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/users")
def create_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user: UserCreateRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Cria um novo usuário para a utilização do sistema

    Args:
        user (UserCreateRequest): Dados do usuário que deseja criar
            {
                name: str, # nome do usuário
                email: EmailStr, # e-mail válido do usuário que será utilizado para autenticar no sistema
                password: str, # senha para autenticar no sistema
            }

    Returns:
        UserResponse: Dados do usuário criado:
            {
                id: int, # Id do criado no banco de dados
                name: str # nome do usuário
                email: str # e-mail do usuário que foi cadastrado no banco de dados
            }


    Raises:

    """
    check_access(token)
    user_added = UserService().add_user(db, user.name, user.email, user.password)
    return user_added


@router.put("/change-password")
def change_password(
    token: Annotated[str, Depends(oauth2_scheme)],
    user: UserChangePasswordRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Altera a senha do usuário que está logado

    Args:
        user (UserChangePasswordRequest): Nova senha que seja informar para o sistema
            {
                new_password: str # nova senha
            }

    Returns:
        dict: Mensagem de retorno:
            {
                "message": "<mensagem de retorno>"
            }

    Raises:
        HTTPException: Se houve falha na alteração da senha.


    """
    try:
        check_access(token)
        user_updated = UserService().change_password(
            db, get_current_user(token), user.new_password
        )
        return {"message": "Senha alterada com sucesso!"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
