from datetime import datetime
from typing import Sequence
from uuid import UUID

from pydantic import BaseModel

from app.adapters.db.orm import Base


class SchemaBase(BaseModel):
    @classmethod
    def from_model(cls, model: Base):
        return cls(**model.to_dict())


class UserSchema(SchemaBase):
    id: UUID
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class TaskSchema(SchemaBase):
    id: UUID
    title: str
    completed: bool
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True


class TaskCollectionSchema(BaseModel):
    tasks: Sequence[TaskSchema]

    class Config:
        arbitrary_types_allowed = True


class TaskCollectionSplittedSchema(BaseModel):
    completed_tasks: Sequence[TaskSchema]
    incompleted_tasks: Sequence[TaskSchema]

    class Config:
        arbitrary_types_allowed = True
