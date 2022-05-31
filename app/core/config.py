from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):  # 1
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URI: Optional[str]


settings = Settings()
