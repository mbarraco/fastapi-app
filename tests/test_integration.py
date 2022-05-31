from asyncio import tasks

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.db.orm import Base
from app.adapters.db.session import db_session, get_engine
from app.api.main import app
from app.domain.models import Task, User

SQLALCHEMY_DATABASE_URL_TEST = (
    "postgresql+asyncpg://postgres:app@db:5432/testdb"
)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def override_db_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        await db.close()


app.dependency_overrides[db_session] = override_db_session


client = TestClient(app)


def test_task_crud_happy_path():
    """Tests User creation, Task creation, Task update (complete and partial)
    adn Task read
    """
    # User creation
    response = client.post(
        "/api/v1/user/", json={"name": "David", "email": "david@bowie.com"}
    )
    assert response.status_code == 201
    user_response = response.json()
    assert user_response["name"] == "David"
    assert user_response["email"] == "david@bowie.com"

    #  Task creation
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "First Task", "owner_id": user_response["id"]},
    )
    assert response.status_code == 201
    task_response = response.json()
    assert task_response["title"] == "First Task"
    assert task_response["owner_id"] == user_response["id"]
    assert task_response["completed"] == False

    task_id = task_response["id"]

    #  Task udpate (partial)
    response = client.put(
        "/api/v1/tasks/", json={"task_id": task_id, "completed": True}
    )
    assert response.status_code == 200
    task_response = response.json()
    assert task_response["title"] == "First Task"
    assert task_response["owner_id"] == user_response["id"]
    assert task_response["completed"] == True

    #  Task Update
    response = client.put(
        "/api/v1/tasks/",
        json={
            "task_id": task_id,
            "completed": False,
            "title": "Updated task",
        },
    )
    assert response.status_code == 200
    task_response = response.json()
    assert task_response["title"] == "Updated task"
    assert task_response["owner_id"] == user_response["id"]
    assert task_response["completed"] == False

    #  Task read
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    task_response = response.json()
    assert task_response["title"] == "Updated task"
    assert task_response["owner_id"] == user_response["id"]
    assert task_response["completed"] == False


def test_task_crud_fail():
    # User creation
    response = client.post(
        "/api/v1/user/", json={"name": "Robert", "email": "robert@fripp.com"}
    )
    assert response.status_code == 201
    user_response = response.json()
    assert user_response["name"] == "Robert"
    assert user_response["email"] == "robert@fripp.com"

    #  Task creation
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "Invalid t4sk", "owner_id": user_response["id"]},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "must contain only letters"
    assert response.json()["detail"][0]["type"] == "value_error"
