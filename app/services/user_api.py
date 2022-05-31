from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.commands import UserCreate
from app.domain.repositories import UserRepository
from app.domain.schema import UserSchema


async def user_create(session: AsyncSession, cmd: UserCreate) -> UserSchema:
    user_model = await UserRepository.create(session, cmd)
    return UserSchema.from_model(user_model)
