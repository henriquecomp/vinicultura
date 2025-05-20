from dataclasses import dataclass


@dataclass()
class AuthResponse():
    email: str
    token: str
