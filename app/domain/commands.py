from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator


def _validate_only_letters(value: str) -> None:
    if not all(x.isalpha() or x.isspace() for x in value):
        raise ValueError("must contain only letters")


class TaskCreate(BaseModel):
    title: str
    owner_id: UUID

    @validator("title")
    def is_letter(cls, v):
        _validate_only_letters(v)
        return v


class TaskUpdate(BaseModel):
    task_id: UUID
    completed: Optional[bool]
    title: Optional[str]

    @validator("title")
    def is_letter(cls, v):
        _validate_only_letters(v)
        return v


class UserCreate(BaseModel):
    name: str
    email: str

    @validator("name")
    def is_letter(cls, v):
        _validate_only_letters(v)
        return v
