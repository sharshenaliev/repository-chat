from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base, get_async_session


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
