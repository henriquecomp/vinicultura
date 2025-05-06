from fastapi import APIRouter
from interfaces.schemas.responses.export_response import ExportResponse
from use_cases.queries.export_scrape import ExportScrape

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


@router.post("/export", response_model=list[ExportResponse])
def create_import() -> list[ExportResponse]:
    use_case = ExportScrape()
    return use_case.execute()


@router.get("/export/{name}")
def get_export():
    return {"message": "Dados recuperado com sucesso"}
