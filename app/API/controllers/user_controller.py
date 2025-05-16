from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from application.DTOs.user_response import UserResponse
from API.models.requests.user_request import UserCreateRequest
from application.services.user_service import UserService
from infrastructure.db.database import get_db
from API.common.check_access import check_access

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/users")
def create_user(token: Annotated[str, Depends(oauth2_scheme)], user: UserCreateRequest, db: Session = Depends(get_db)):
    check_access(token)
    user_added = UserService().add_user(db, user.name, user.email, user.password)
    return user_added


@router.get("/users/{email}", response_model=UserResponse)
def get_user(
    # email: str, use_case: GetUserByEmailQuery = Depends(get_query_use_case)
):
    # user = use_case.execute(email)
    # if not user:
    #    raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # return user
    pass
