from domain.repositories.user_repository import UserRepository
from domain.entities.user import User


class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, name: str, email: str):
        user = User(id=None, name=name, email=email)
        self.repository.save(user)
