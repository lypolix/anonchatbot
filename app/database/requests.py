from app.database.models import async_session
from app.database.models import User, Message
from sqlalchemy import select, update, delete
from sqlalchemy import func


async def set_user(tg_id : int, username: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id, username = username))
            await session.commit() 

async def set_message(text: str, user1: int, user2: int) -> None:
    async with async_session() as session:
        
        session.add(Message(text=text, user1=user1, user2=user2))
        await session.commit()

async def get_id_by_username(username: str) -> int | None:

    async with async_session() as session:
        result = await session.scalar(select(User.tg_id).where(func.lower(User.username) == username.lstrip('@')))
        return result

async def get_first_message(tg_id: int) -> Message | None:

    async with async_session() as session:
        return await session.scalar(select(Message).where(Message.user2 == tg_id).order_by(Message.id).limit(1))

async def delete_message(message_id: int):
    
    async with async_session() as session:
        await session.execute(delete(Message).where(Message.id == message_id))

        await session.commit()