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
        """
        Serviço que trata os dados do usuario para criar na base de dados

        Args:
            name: str, # nome do usuário que será cadastrado
            email: str, # e-mail do usuário que será cadastrado
            password: str # senha do usuário que será cadastrado

        Returns:
            UserResponse: Dados do usuário criado:
                {
                    id: int, # Id do criado no banco de dados
                    name: str # nome do usuário
                    email: str # e-mail do usuário que foi cadastrado no banco de dados
                }

        Raises:
            

        """
        passHashed = self._hash_password(password)
        user = User(name=name, email=email, password=passHashed)
        added = UserRepositorySQL(db).save(user)
        return UserResponse(
            id=added.id,
            name=user.name,
            email=user.email,
        )

    def auth_by_email(self, db: Session, email: str, password: str) -> AuthResponse:
        """
        Serviço que trata os dados do usuario de autenticação do usuario

        Args:            
            email: str, # e-mail do usuário que será autenticado
            password: str # senha do usuário que será autenticado

        Returns:
            AuthResponse: Dados do usuário autenticado:
                {
                    email: str # e-mail do usuário que foi autenticado
                    token: str # token gerado para o usuário autenticado comunicar com a aplicação
                }

        Raises:

        """        
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
        """
        Serviço que trata a alteração de senha do usuário autenticado

        Args:            
            email: str, # e-mail do usuário que a senha será alterada
            password: str # nova senha do usuário

        Returns:
            AuthResponse: Dados do usuário autenticado:
                {
                    email: str # e-mail do usuário que foi autenticado
                    token: str # token gerado para o usuário autenticado comunicar com a aplicação
                }

        Raises:
            Exception: caso o usuário não seja encontrado no banco de dados
            Exception: caso a senha seja igual a atual

        """              
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
        """
        Método privado que criptografa a senha para salvar no banco de dados

        Args:                        
            password: str # nova senha do usuário

        Returns:
            str: senha criptografada

        Raises:

        """               
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def _check_password(self, password: str, hashed: str) -> str:
        """
        Método privado que checa se a senha enviada é igual a criptografada

        Args:                        
            password: str # senha do usuário informada pelo usuário na autenticação
            hashed: str # senha criptografada gravada no banco de dados

        Returns:
            bool: True # se a senha é valida
                  False # se a senha é inválida

        Raises:

        """            
        if not verify_password(password, hashed):
            return False

        return True
