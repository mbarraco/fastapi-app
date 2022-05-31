#  Base has them before Alembic imports it
from app.adapters.db.orm import Base
from app.domain.models import Task, User
