from pydantic import BaseModel


class UserChangePasswordRequest(BaseModel):
    new_password: str
