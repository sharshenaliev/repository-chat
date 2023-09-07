from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from datetime import datetime

from src.auth.auth import auth_backend
from src.auth.database import User
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from src.database import get_async_session
from src.routers import router
from src.models import user, message
from src.orm import get_or_create
from src.schemas.userchatmessage import CreateMessage

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(title='Test')

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.post("/message")
async def protected_route(new_message: CreateMessage,
                          my_user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)):
    query = select(user).where(user.c.id == new_message.receiver_id)
    result = await session.execute(query)
    if result.scalars().all():
        chat_id = await get_or_create(my_user, new_message.receiver_id, session)
        new_message = new_message.dict()
        new_message['sender_id'] = my_user.id
        new_message['time_delivered'] = datetime.now()
        new_message['chat_id'] = chat_id
        stmt = insert(message).values(**new_message)
        await session.execute(stmt)
        await session.commit()
        return {"status": "message sent"}
    else:
        return {"message": "no such user"}


app.include_router(router)
