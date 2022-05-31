from functools import wraps

from asyncpg.exceptions import IntegrityConstraintViolationError
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

INTEGRITY_CONSTRAINT_ERROR_MESSAGES = {
    "_task_title_owner_uc": "Task title must be unique",
    "tasks_owner_id_fkey": "Invalid user",
}


def format_errors(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            handle_error(e)

    return wrapped


def handle_error(exc: Exception) -> None:

    if isinstance(exc, IntegrityError):
        if isinstance(exc.orig.__context__, IntegrityConstraintViolationError):
            constraint_name = exc.orig.__context__.as_dict().get(
                "constraint_name"
            )
            if (
                constraint_name
                and constraint_name in INTEGRITY_CONSTRAINT_ERROR_MESSAGES
            ):
                raise HTTPException(
                    status_code=409,
                    detail=INTEGRITY_CONSTRAINT_ERROR_MESSAGES[constraint_name],
                )
    raise
