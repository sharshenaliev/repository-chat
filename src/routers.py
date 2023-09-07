from fastapi import APIRouter, Depends
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import user, chat, message
from src.schemas.user import User
from src.schemas.userchat import UserChat
from src.schemas.userchatmessage import UserChatMessage


router = APIRouter(
    prefix="/users",
    tags=["Operation"]
)


@router.get("/", response_model=list[User], response_model_exclude=["hashed_password"])
async def get_list_users(pk: int = 0, username: str = 'all', session: AsyncSession = Depends(get_async_session)):
    if pk == 0 and username == 'all':
        query = select(user)
    elif pk != 0 and username == 'all':
        query = select(user).where(user.c.id == pk)
    elif pk == 0 and username != 'all':
        query = select(user).where(user.c.username == username)
    else:
        query = select(user).where(user.c.id == pk and user.c.username == username)
    result = await session.execute(query)
    return result.all()


@router.get("/chats", response_model=list[UserChat])
async def get_list_chats(status: bool = None, session: AsyncSession = Depends(get_async_session)):
    user1 = aliased(user)
    user2 = aliased(user)
    if status is None:
        query = select(chat).join(user1, chat.c.user_id == user1.c.id)\
            .add_columns(user1.c.username.label('user_username'))\
            .join(user2, chat.c.interlocutor_id == user2.c.id)\
            .add_columns(user2.c.username.label('interlocutor_username'))
    else:
        query = select(chat).join(user1, chat.c.user_id == user1.c.id)\
            .add_columns(user1.c.username.label('user_username')) \
            .join(user2, chat.c.interlocutor_id == user2.c.id)\
            .add_columns(user2.c.username.label('interlocutor_username'))\
            .where(chat.c.status == status)
    result = await session.execute(query)
    return result.all()


@router.get("/chats/number")
async def get_number_chats(session: AsyncSession = Depends(get_async_session)):
    query = select(chat)
    result = await session.execute(query)
    return f"Chats number is {len(result.all())}"


@router.get("/messages", response_model=list[UserChatMessage])
async def get_list_chats(sender_id: int = 0, receiver_id: int = 0, time_delivered: datetime = None, session: AsyncSession = Depends(get_async_session)):
    if sender_id == 0 and receiver_id == 0 and time_delivered is None:
        query = select(message)
    elif sender_id != 0 and receiver_id == 0 and time_delivered is None:
        query = select(message).where(message.c.sender_id == sender_id)
    elif sender_id == 0 and receiver_id != 0 and time_delivered is None:
        query = select(message).where(message.c.receiver_id == receiver_id)
    elif sender_id == 0 and receiver_id == 0 and time_delivered is not None:
        query = select(message).where(message.c.time_delivered == time_delivered)
    elif sender_id != 0 and receiver_id != 0 and time_delivered is None:
        query = select(message).where(message.c.sender_id == sender_id and message.c.receiver_id == receiver_id)
    elif sender_id != 0 and receiver_id == 0 and time_delivered is not None:
        query = select(message).where(message.c.sender_id == sender_id and message.c.time_delivered == time_delivered)
    elif sender_id == 0 and receiver_id != 0 and time_delivered is not None:
        query = select(message).where(message.c.receiver_id == receiver_id and message.c.time_delivered == time_delivered)
    else:
        query = select(message).where(message.c.sender_id == sender_id and message.c.receiver_id == receiver_id and message.c.time_delivered == time_delivered)
    result = await session.execute(query)
    return result.all()


@router.get("/chats/messages")
async def get_number_chats(pk: int, session: AsyncSession = Depends(get_async_session)):
    query = select(message).where(message.c.chat_id == pk)
    result = await session.execute(query)
    return f"Messages number is {len(result.all())} in chat {pk}"
