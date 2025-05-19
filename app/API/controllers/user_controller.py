from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from application.DTOs.user_response import UserResponse
from API.models.requests.user_create_request import UserCreateRequest
from API.models.requests.user_change_password_request import UserChangePasswordRequest
from application.services.user_service import UserService
from infrastructure.db.database import get_db
from API.common.check_access import check_access, get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/users")
def create_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user: UserCreateRequest,
    db: Session = Depends(get_db),
):
    check_access(token)
    user_added = UserService().add_user(
        db, user.name, user.email, user.password
    )
    return user_added


@router.put("/change-password")
def change_password(
    token: Annotated[str, Depends(oauth2_scheme)],
    user: UserChangePasswordRequest,
    db: Session = Depends(get_db),
):
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
