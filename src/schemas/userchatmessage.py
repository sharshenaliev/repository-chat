from datetime import datetime
from pydantic import BaseModel
from src.schemas.user import User
from src.schemas.userchat import UserChat


class UserChatMessage(BaseModel):
    id: int
    text: str
    sender_id: int
    receiver_id: int
    time_delivered: datetime
    chat_id: int


class CreateMessage(BaseModel):
    text: str
    receiver_id: int
