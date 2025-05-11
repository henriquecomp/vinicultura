from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from API.models.requests.user_request import UserCreateRequest
from API.models.responses.user_response import UserResponse
from application.commands.create_user import CreateUserUseCase
from application.queries.get_user_by_email import GetUserByEmailQuery
from infrastructure.repositories.user_repository_sql import UserRepositorySQL
from infrastructure.db.database import get_db

router = APIRouter()


def get_command_use_case(session: Session = Depends(get_db)):
    return CreateUserUseCase(UserRepositorySQL(session))


def get_query_use_case(session: Session = Depends(get_db)):
    return GetUserByEmailQuery(UserRepositorySQL(session))


@router.post("/users", response_model=dict)
def create_user(
    user: UserCreateRequest, use_case: CreateUserUseCase = Depends(get_command_use_case)
):
    use_case.execute(user.name, user.email)
    return {"message": "Usuário criado com sucesso"}


@router.get("/users/{email}", response_model=UserResponse)
def get_user(
    email: str, use_case: GetUserByEmailQuery = Depends(get_query_use_case)
):
    user = use_case.execute(email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
