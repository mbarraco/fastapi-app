from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.commands import TaskCreate, TaskUpdate
from app.domain.repositories import TaskRepository
from app.domain.schema import TaskSchema


async def task_create(session: AsyncSession, cmd: TaskCreate) -> TaskSchema:
    model = await TaskRepository.create(session, cmd)
    return TaskSchema.from_model(model) if model else None


async def task_retrieve(
    session: AsyncSession, task_id: UUID
) -> Optional[TaskSchema]:
    model = await TaskRepository.get(session, task_id)
    return TaskSchema.from_model(model) if model else None


async def task_retrieve_all(session: AsyncSession) -> List[TaskSchema]:
    models = await TaskRepository.get_all(session)
    return [TaskSchema.from_model(m) for m in models]


async def task_update(
    session: AsyncSession, cmd: TaskUpdate
) -> Optional[TaskSchema]:
    task = await TaskRepository.get(session, cmd.task_id)
    if task is None:
        raise ValueError(f"task not found for id: {cmd.task_id}")

    is_dirty = False
    if cmd.completed is not None and task.completed != cmd.completed:
        task.completed = cmd.completed
        is_dirty = True
    if cmd.title is not None and task.title != cmd.title:
        task.title = cmd.title
        is_dirty = True
    if is_dirty:
        task = await TaskRepository.update(session, task)

    return TaskSchema.from_model(task)
