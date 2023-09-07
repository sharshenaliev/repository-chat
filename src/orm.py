from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.models import chat

from fastapi import Depends


async def get_or_create(user, interlocutor, session: AsyncSession = Depends(get_async_session)):
    query_1 = select(chat).where(chat.c.user_id == user.id, chat.c.interlocutor_id == interlocutor)
    result_1 = await session.execute(query_1)
    instance_1 = result_1.all()
    query_2 = select(chat).where(chat.c.user_id == interlocutor, chat.c.interlocutor_id == user.id)
    result_2 = await session.execute(query_2)
    instance_2 = result_2.all()
    if instance_1:
        return instance_1[0][0]
    elif instance_2:
        return instance_2[0][0]
    else:
        stmt = insert(chat).values(user_id=user.id, interlocutor_id=interlocutor)
        await session.execute(stmt)
        await session.commit()
        query = select(chat).where(chat.c.user_id == user.id, chat.c.interlocutor_id == interlocutor)
        result = await session.execute(query)
        instance = result.all()
        return instance[0][0]
