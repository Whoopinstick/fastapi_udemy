from todo.models import Todos
from fastapi import status
from .utils import client, TestingSessionLocal, test_todo


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

def test_update_todo_authenticated(test_todo):
    request_data = {
        'complete': False, 'description': 'updated todo', "priority": 3, "title": "todo change"
    }

    response = client.put("/todos/1", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo_not_found_authenticated(test_todo):
    request_data = {
        'complete': False, 'description': 'updated todo', "priority": 3, "title": "todo change"
    }

    response = client.put("/todos/999", json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}

def test_delete_todo_authenticated(test_todo):
    response = client.delete("/todos/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
