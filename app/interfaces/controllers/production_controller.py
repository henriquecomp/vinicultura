from fastapi import APIRouter
from interfaces.schemas.responses.production_response import ProductionResponse
from use_cases.queries.production_scrape import ProductionScrape

# from sqlalchemy.orm import Session
# from interfaces.schemas.requests.user_create_request import UserCreateRequest
# from interfaces.schemas.responses.user_response import UserResponse
# from use_cases.commands.create_user import CreateUserUseCase
# from use_cases.queries.get_user_by_email import GetUserByEmailQuery
# from adapters.repositories.user_repository_sql import UserRepositorySQL
# from adapters.db.database import get_db

router = APIRouter()


# def get_command_use_case(session: Session = Depends(get_db)):
#     return CreateUserUseCase(UserRepositorySQL(session))


# def get_query_use_case(session: Session = Depends(get_db)):
# return GetUserByEmailQuery(UserRepositorySQL(session))


@router.post("/production", response_model=list[ProductionResponse])
def create_production() -> list[ProductionResponse]:
    use_case = ProductionScrape()
    return use_case.execute()


@router.get("/production/{name}")
def get_production():
    return {"message": "Dados recuperado com sucesso"}
