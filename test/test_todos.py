import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from main import app
from todo.database import Base, get_db
from todo.models import Todos
from todo.oath2 import get_current_user
from fastapi.testclient import TestClient
from fastapi import status

SQLALCHEMY_DATABASE_URL = 'sqlite:///todo/test_todos.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username": "tester", "id": 1, "user_role": "admin"}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="first todo",
        description="my first todo",
        priority=3,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

def test_root(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Hello": "Todos"}

def test_read_all_todo_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ==  [{'complete': False, 'description': 'my first todo', 'id': 1, 'owner_id': 1,
                                "priority": 3, "title": "first todo"}]

def test_read_one_todo_authenticated(test_todo):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'description': 'my first todo', 'id': 1, 'owner_id': 1,
                                "priority": 3, "title": "first todo"}

def test_read_one_todo_not_found_authenticated(test_todo):
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}

def test_create_todo_authenticated(test_todo):
    request_data = {
        'complete': False, 'description': 'my second todo',"priority": 5, "title": "second todo"
    }

    response = client.post("/todos", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')



