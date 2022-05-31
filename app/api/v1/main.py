from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from app.adapters.db.session import db_session
from app.api.exceptions import format_errors
from app.domain.commands import TaskCreate, TaskUpdate, UserCreate
from app.domain.schema import TaskCollectionSchema, TaskSchema, UserSchema
from app.services.task_api import (task_create, task_retrieve,
                                   task_retrieve_all, task_update)
from app.services.user_api import user_create

api_router = APIRouter()


@api_router.post("/tasks/", status_code=201, response_model=TaskSchema)
@format_errors
async def create_task(
    *, cmd: TaskCreate, session=Depends(db_session)
) -> TaskSchema:
    task = await task_create(session, cmd)
    await session.close()
    return task


@api_router.post("/user/", status_code=201, response_model=UserSchema)
@format_errors
async def create_user(
    *, cmd: UserCreate, session=Depends(db_session)
) -> UserSchema:
    user = await user_create(session, cmd)
    await session.close()
    return user


@api_router.get("/tasks/{task_id}", status_code=200, response_model=TaskSchema)
@format_errors
async def get_task(
    task_id: UUID, session=Depends(db_session)
) -> Optional[TaskSchema]:
    task = await task_retrieve(session, task_id)
    return task


@api_router.get("/tasks/", status_code=200, response_model=TaskCollectionSchema)
@format_errors
async def get_tasks() -> TaskCollectionSchema:
    #  TODO: test
    async with db_session() as session:
        tasks = await task_retrieve_all(session)
    return TaskCollectionSchema(tasks=tasks)


@api_router.put("/tasks/", status_code=200, response_model=TaskSchema)
@format_errors
async def update_task(
    *, cmd: TaskUpdate, session=Depends(db_session)
) -> Optional[TaskSchema]:
    task = await task_update(session, cmd)
    await session.close()
    return task
