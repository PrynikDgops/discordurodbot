import json
import logging
from typing import Optional, List, Type

from sqlalchemy import create_engine, Column, Integer, Boolean, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

engine = create_engine(f"sqlite:///UrodCity.db")

Base = declarative_base()


class TownMember(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    required = Column(Boolean)
    workers = Column(Text, default="[]")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


async def add_member(discord_id: int) -> None:
    member = TownMember(discord_id=discord_id)
    session.add(member)
    session.commit()
    logger.info(msg=f"Добавлен новый житель {discord_id}")


async def add_user_if_not_exists(discord_id: int) -> None:
    user = session.query(TownMember).filter_by(discord_id=discord_id).first()
    if not user:
        await add_member(discord_id=discord_id)


async def remove_member(discord_id: int) -> None:
    member = session.query(TownMember).filter_by(discord_id=discord_id).first()
    if member:
        session.delete(member)
        session.commit()
        logger.info(msg=f"Данные жителя удалены || {discord_id}")


async def get_all_users() -> List[Type[TownMember]]:
    response = session.query(TownMember).all()
    return response


async def add_new_task(message_id: int, required: bool) -> None:
    task = Task(message_id=message_id, required=required)
    session.add(task)
    session.commit()


async def add_worker(message_id: int, user_id: int):
    task = session.query(Task).filter_by(message_id=message_id).first()
    workers = json.loads(task.workers)
    workers.append(user_id)
    task.workers = json.dumps(workers)
    session.commit()


async def remove_worker(message_id: int, user_id: int):
    task = session.query(Task).filter_by(message_id=message_id).first()
    workers = json.loads(task.workers)
    workers.remove(user_id)
    task.workers = json.dumps(workers)
    session.commit()


async def get_task_workers(message_id: int) -> Optional[List[int]]:
    task = session.query(Task).filter_by(message_id=message_id).first()
    if not task:
        return None
    workers = json.loads(task.workers)
    return workers


async def get_task(message_id: int) -> Optional[Task]:
    task = session.query(Task).filter_by(message_id=message_id).first()
    return task


async def remove_task(message_id: int):
    task = session.query(Task).filter_by(message_id=message_id).first()
    if task:
        session.delete(task)
        session.commit()