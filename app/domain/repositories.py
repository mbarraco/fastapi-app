from typing import Generic, Iterable, List, Optional, Type, TypeVar
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.orm import Base
from app.domain.models import Task, User

T = TypeVar("T")
ModelT = TypeVar("ModelT", bound=Base)
CreateModelT = TypeVar("CreateModelT", bound=BaseModel)
UpdateModelT = TypeVar("UpdateModelT", bound=BaseModel)


class Repository(Generic[ModelT]):

    model: Type[ModelT]

    @classmethod
    async def get(cls, session: AsyncSession, _id: UUID) -> Optional[ModelT]:
        stmt = select(cls.model).where(cls.model.id == str(_id))
        res = await session.execute(stmt)
        return res.scalar()

    @classmethod
    async def get_all(cls, session: AsyncSession) -> Optional[ModelT]:
        stmt = select(cls.model)
        res = await session.execute(stmt)
        return res.scalars().all()

    @classmethod
    async def get_by_ids(
        cls, session: AsyncSession, ids: Iterable[UUID]
    ) -> Optional[ModelT]:
        items: List[ModelT] = []
        stmt = select(cls.model).where(cls.model.id.in_(ids))
        res = await session.execute(stmt)
        items = res.scalars().all()
        return items

    @classmethod
    async def create(
        cls, session: AsyncSession, obj_in: CreateModelT
    ) -> ModelT:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = cls.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @classmethod
    async def update(cls, session: AsyncSession, item: ModelT) -> ModelT:
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item


class UserRepository(Repository[User]):
    model = User


class TaskRepository(Repository[Task]):
    model = Task
