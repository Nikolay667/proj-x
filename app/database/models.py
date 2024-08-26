from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url = 'sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

#for pandas in file requests.py
import sqlite3

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Card(Base):
    __tablename__ = 'Cards'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column()
    rarity: Mapped[str] = mapped_column(String(20))
    points: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String(300))
    img_link: Mapped[str] = mapped_column()
    proj_link: Mapped[str] = mapped_column()

class User(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key = True)
    tg_id = mapped_column(BigInteger)
    card_id: Mapped[int] = mapped_column()
    card_link: Mapped[str] = mapped_column()

class Time(Base):
    __tablename__ = 'Time'

    id: Mapped[int] = mapped_column(primary_key = True)
    tg_id = mapped_column(BigInteger)
    time: Mapped[str] = mapped_column()

class Rating(Base):
    __tablename__ = 'Rating'

    #id: Mapped[int] = mapped_column()
    tg_id = mapped_column(BigInteger)
    points: Mapped[int] = mapped_column(primary_key=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)