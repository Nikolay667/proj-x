from app.database.models import async_session
from sqlalchemy.orm import sessionmaker, scoped_session
from app.database.models import User, Card, Time, Rating
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, desc
from sqlalchemy import select, update, asc
from app.database.models import engine

import pandas as pd
from app.database.models import con

import asyncio
import random


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id))
            await session.commit()
        #print(user)

async def to_collection(cardId, tgId, c_link):
    async with async_session() as session:
        session.add(User(card_id = cardId, tg_id = tgId, card_link = c_link))
        await session.commit()

async def get_card():
    async with async_session() as session:
        card_id = random.randint(1,5)
        #card_id = 3
        card_link = await session.scalar(select(Card.img_link).where(Card.id == card_id))
        card_name = await session.scalar(select(Card.name).where(Card.id == card_id))
        card_rarity = await session.scalar(select(Card.rarity).where(Card.id == card_id))
        card_points = await session.scalar(select(Card.points).where(Card.id == card_id))
        card_description = await session.scalar(select(Card.description).where(Card.id == card_id))
        proj_link = await session.scalar(select(Card.proj_link).where(Card.id == card_id))
        return [card_link, card_name, card_rarity, card_points, card_description, card_id, proj_link]

async def collection_cards(tgId):
    async with async_session() as session:
        card_from_User = await session.scalars(select(User.card_id).where(User.tg_id == tgId))
        #card_from_Card = await session.scalars(select(Card).where(Card.id == card_from_User))
        return list(card_from_User)
    
async def details_collection_cards(cardId):
    async with async_session() as session:
        card_link = await session.scalar(select(Card.img_link).where(Card.id == cardId))
        card_name = await session.scalar(select(Card.name).where(Card.id == cardId))
        card_rarity = await session.scalar(select(Card.rarity).where(Card.id == cardId))
        card_points = await session.scalar(select(Card.points).where(Card.id == cardId))
        card_description = await session.scalar(select(Card.description).where(Card.id == cardId))
        proj_link = await session.scalar(select(Card.proj_link).where(Card.id == cardId))
        return [card_link, card_name, card_rarity, card_points, card_description, cardId, proj_link]

async def time_check(l_r, tgId):
    async with async_session() as session:
        session.add(Time(time = l_r, tg_id = tgId))
        await session.commit()

async def time_check2(tgId):
    async with async_session() as session:
        check_time = await session.scalar(select(Time.time).where(Time.tg_id == tgId))
        if not check_time:
            return int(0)
        else:
            return check_time

async def delete_time_check(tgId):
    async with async_session() as session:
        time_to_delete = await session.scalar(select(Time).where(Time.tg_id == tgId))
        await session.delete(time_to_delete)
        await session.commit()


#points funcitons:

async def create_points(tgId, points):
    async with async_session() as session:
        session.add(Rating(tg_id = tgId, points = points))
        await session.commit()

async def delete_points(tgId):
    async with async_session() as session:
        info = await session.scalar(select(Rating).where(Rating.tg_id == tgId))
        await session.delete(info)
        await session.commit()

async def add_points(tgId, point):
    async with async_session() as session:
        session.add(Rating(tg_id = tgId, points = point))
        await session.commit()

async def view_points(tgId):
    async with async_session() as session:
        points = await session.scalar(select(Rating.points).where(Rating.tg_id == tgId))
        return points


#below - python pandas
async def rating_place(tgId):
    df = pd.read_sql("SELECT * FROM Rating", con)
    row_index = df.loc[df['tg_id'] == tgId].index[0]
    return (int(row_index)+1)