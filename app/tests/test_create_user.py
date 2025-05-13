from application.DTOs.create_user import UserResponse
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

class FakeRepository(UserRepository):
    def __init__(self):
        self.saved_users = []

    def save(self, user: User) -> None:
        self.saved_users.append(user)

def test_create_user():
    repo = FakeRepository()
    use_case = CreateUserUseCase(repo)
    use_case.execute("Alice", "alice@example.com")
    assert len(repo.saved_users) == 1
    assert repo.saved_users[0].name == "Alice"