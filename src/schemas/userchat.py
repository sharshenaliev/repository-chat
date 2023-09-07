from pydantic import BaseModel
from src.schemas.user import User
from typing import Optional


class UserChat(BaseModel):
    id: int
    user_id: int
    interlocutor_id: int
    status: bool
    user_username: str
    interlocutor_username: str

