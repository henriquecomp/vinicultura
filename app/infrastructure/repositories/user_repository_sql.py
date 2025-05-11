from sqlalchemy.orm import Session
from sqlalchemy.future import select
from domain.repositories.user_repository import UserRepository
from domain.entities.user import User


class UserRepositorySQL(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()

    def get_by_email(self, email: str) -> User:
        result = self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()
