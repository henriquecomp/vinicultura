import bcrypt
from sqlalchemy.orm import Session
from application.DTOs.user_response import UserResponse
from application.DTOs.auth_response import AuthResponse
from domain.entities.user import User
from infrastructure.repositories.user_repository_sql import UserRepositorySQL
from application.services.security_service import create_access_token, verify_password


class UserService:
    def add_user(
        self, db: Session, name: str, email: str, password: str
    ) -> UserResponse:
        passHashed = self._hash_password(password)
        user = User(name=name, email=email, password=passHashed)
        added = UserRepositorySQL(db).save(user)
        return UserResponse(
            id=added.id,
            name=user.name,
            email=user.email,
        )

    def auth_by_email(self, db: Session, email: str, password: str) -> AuthResponse:
        user = UserRepositorySQL(db).get_by_email(email)
        isValid = self._check_password(password, user.password)

        if not isValid:
            return None

        token = create_access_token(data={"sub": user.email})
        if not user:
            return None
        return AuthResponse(
            email=user.email,
            token=token,
        )

    def change_password(self, db: Session, email: str, password: str) -> UserResponse:
        user = UserRepositorySQL(db).get_by_email(email)
        if not user:
            raise Exception("Usuário não encontrado")

        if self._check_password(password, user.password):
            raise Exception("A nova senha não pode ser igual a senha atual")

        user.password = self._hash_password(password)
        updated_user = UserRepositorySQL(db).update(user)

        return UserResponse(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
        )

    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def _check_password(self, password: str, hashed: str) -> str:
        if not verify_password(password, hashed):
            return False

        return True
