from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


metadata = MetaData()

Base = declarative_base()


user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String, nullable=False, unique=True),
    Column('hashed_password', String, nullable=False),
    Column('email', String, nullable=False, unique=True),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
)

chat = Table(
    'chat',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('interlocutor_id', Integer, ForeignKey('user.id')),
    Column('status', Boolean, default=True),
)

message = Table(
    'message',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('text', String),
    Column('sender_id', Integer, ForeignKey("user.id")),
    Column('receiver_id', Integer, ForeignKey("user.id")),
    Column('time_delivered', TIMESTAMP, default=datetime.utcnow),
    Column('chat_id', Integer, ForeignKey('chat.id')),
)
