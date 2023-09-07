from sqlalchemy import insert, select
from src.models import user, chat
from conftest import client, async_session_maker
from datetime import datetime
from tests.test_auth import test_login


async def test_users():
    async with async_session_maker() as session:
        stmt = insert(user).values(username="test", email="test", hashed_password="test")
        await session.execute(stmt)
        await session.commit()

        query = select(*[c for c in user.c if c.name != 'hashed_password'])
        result = await session.execute(query)
        assert result.all() == [(1, "string", "string", True, False, False), (2, "test", "test", True, False, False)]


async def test_users_list():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'username': 'string', 'email': 'string',
                                'is_active': True, 'is_superuser': False, 'is_verified': False},
                               {'id': 2, 'username': 'test', 'email': 'test', 'is_active': True,
                                'is_superuser': False, 'is_verified': False}]


async def test_users_list_filter():
    response = client.get("/users?pk=2")
    assert response.status_code == 200
    assert response.json() == [{'id': 2, 'username': 'test', 'email': 'test', 'is_active': True,
                                'is_superuser': False, 'is_verified': False}]


async def test_create_message():
    response = client.post("/message", json={
        "text": "text",
        "receiver_id": 2,
    }, headers=test_login())
    assert response.status_code == 200


#не удается приравнять миллисекунды в поле времени
async def test_messages_list():
    response = client.get("/users/messages")
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'text': 'text', 'sender_id': 1, 'receiver_id': 2,
                               'time_delivered': datetime.now().isoformat(), 'chat_id': 1}


async def test_chats_list():
    async with async_session_maker() as session:
        stmt = insert(user).values(username="user", email="user", hashed_password="user")
        await session.execute(stmt)
        await session.commit()
        stmt = insert(chat).values(user_id=1, interlocutor_id=3)
        await session.execute(stmt)
        await session.commit()

        query = select(chat)
        result = await session.execute(query)
        assert result.all() == [(1, 1, 2, True), (2, 1, 3, True)]


async def test_chat_list():
    response = client.get("/users/chats")
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'interlocutor_id': 2, 'interlocutor_username': 'test', 'status': True,
                                'user_id': 1, 'user_username': 'string'},
                               {'id': 2, 'interlocutor_id': 3, 'interlocutor_username': 'user', 'status': True,
                                'user_id': 1, 'user_username': 'string'}]


async def test_chat_list_filter():
    response = client.get("/users/chats?status=False")
    assert response.status_code == 200
    assert response.json() == []


async def test_chat_number():
    response = client.get("/users/chats/number")
    assert response.status_code == 200
    assert response.json() == 'Chats number is 2'


async def test_chat_message():
    response = client.get("/users/chats/messages?pk=1")
    assert response.status_code == 200
    assert response.json() == 'Messages number is 1 in chat 1'
