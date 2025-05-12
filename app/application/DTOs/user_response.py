from dataclasses import dataclass


@dataclass()
class UserResponse():
    id: int
    name: str
    email: str
