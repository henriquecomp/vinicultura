import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


def hash_password(password: str) -> str:     
    """
    Serviço que criptografa a senha enviada

    Args:
        password: str, # senha a ser criptografada
        
    Returns:
        str: Senha criptografada
            
    Raises:

    """    
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Serviço que verifica se uma senha em texto puro é igual a senha criptografada

    Args:
        plain_password: str, # senha em texto puro
        hashed_password: str # senha criptografada
        
    Returns:
        bool: True, se as senhas forem iguais
              False, se a senhas forem diferentes
            
    Raises:

    """        
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Cria um token para representar o usuário autenticado

    Args:
        data: dict, # e-mail do usuário para adicionar a propriedade sub do token
        expires_delta: timedelta # tempo de expiração do token
        
    Returns:
        string: Token válido para acesso posterior
                          
    Raises:

    """        
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    """
    Decodifica o token para ler as informações do usuário logado

    Args:
        token: str, # token enviado durante a autenticação para o usuário
        expires_delta: timedelta # tempo de expiração do token   

    Returns:
        dict[str, Any]: propriedades do token
                          
    Raises:
        Exception: caso não consiga realizar a decodificação do token

    """       
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise Exception(status_code=500, detail="Invalid token")
        
