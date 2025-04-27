from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from interfaces.schemas.requests.user_create_request import UserCreateRequest
from interfaces.schemas.responses.user_response import UserResponse
from use_cases.commands.create_user import CreateUserUseCase
from use_cases.queries.get_user_by_email import GetUserByEmailQuery
from adapters.repositories.user_repository_sql import UserRepositorySQL
from adapters.db.database import get_db

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
