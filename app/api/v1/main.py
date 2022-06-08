import asyncio
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from app.adapters.db.session import db_session
from app.api.exceptions import format_errors
from app.domain.commands import TaskCreate, TaskUpdate, UserCreate
from app.domain.schema import (TaskCollectionSchema,
                               TaskCollectionSplittedSchema, TaskSchema,
                               UserSchema)
from app.services.task_api import (task_create, task_retrieve,
                                   task_retrieve_all,
                                   task_retrieve_by_completion, task_update)
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
async def get_tasks(
    task_id: UUID = None, session=Depends(db_session)
) -> TaskCollectionSchema:
    if task_id is not None:
        tasks = [await task_retrieve(session, task_id)]
    else:
        tasks = await task_retrieve_all(session)

    await session.close()
    return TaskCollectionSchema(tasks=tasks)


@api_router.get(
    "/tasks-splitted/",
    status_code=200,
    response_model=TaskCollectionSplittedSchema,
)
@format_errors
async def get_tasks_splitted(
    session=Depends(db_session), completed: bool = None
) -> TaskCollectionSplittedSchema:
    if completed is None:
        completed_tasks, incompleted_tasks = await asyncio.gather(
            task_retrieve_by_completion(session, True),
            task_retrieve_by_completion(session, False),
        )
    else:
        tasks = task_retrieve_by_completion(session, completed)
        if completed:
            completed_tasks, incompleted_tasks = tasks, None
        else:
            completed_tasks, incompleted_tasks = None, tasks

    await session.close()
    return TaskCollectionSplittedSchema(
        completed_tasks=completed_tasks, incompleted_tasks=incompleted_tasks
    )


@api_router.put("/tasks/", status_code=200, response_model=TaskSchema)
@format_errors
async def update_task(
    *, cmd: TaskUpdate, session=Depends(db_session)
) -> Optional[TaskSchema]:
    task = await task_update(session, cmd)
    await session.close()
    return task
