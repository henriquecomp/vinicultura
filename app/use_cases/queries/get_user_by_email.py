from domain.repositories.user_repository import UserRepository
from domain.entities.user import User


class GetUserByEmailQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, email: str) -> User:
        return self.repository.get_by_email(email)
