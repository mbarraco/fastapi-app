from uuid import uuid4

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, String,
                        UniqueConstraint, text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.adapters.db.orm import Base


class User(Base):
    id = Column(UUID, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(256), nullable=False)
    email = Column(String, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    tasks = relationship(
        "Task",
        cascade="all,delete-orphan",
        back_populates="owner",
        uselist=True,
    )


class Task(Base):
    id = Column(UUID, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String(256), nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    owner_id = Column(UUID, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    owner = relationship("User", back_populates="tasks")

    __table_args__ = (
        UniqueConstraint("title", "owner_id", name="_task_title_owner_uc"),
    )
