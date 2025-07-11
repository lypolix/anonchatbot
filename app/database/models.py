from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import String

engine = create_async_engine(url = 'sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key = True)
    tg_id: Mapped[int] = mapped_column(BigInteger) 
    username: Mapped[str] = mapped_column(String(25))

class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key = True)
    text: Mapped[str] = mapped_column(String(120))
    user1: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user2: Mapped[int] = mapped_column(ForeignKey('users.id'))

async def async_main():
    async with engine.begin() as const:
        await const.run_sync(Base.metadata.create_all)

