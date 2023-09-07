from pydantic import BaseModel, Field, EmailStr, SecretStr


class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: SecretStr = Field(exclude=True)
    is_active: bool
    is_superuser: bool
    is_verified: bool
