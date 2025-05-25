from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User


class UserRepositorySQL(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user: User) -> User:
        self.session.merge(user)
        self.session.commit()
        return user

    def get_by_email(self, email: str) -> User:
        result = self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()
