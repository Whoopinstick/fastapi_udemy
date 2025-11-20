from fastapi import status
from todo.routers.admin import get_db, get_current_user
from .utils import client, test_todo, app, override_get_db, override_get_current_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# TODO: Fix tests to admin routes

def test_admin_read_all_todo_authenticated(test_todo):
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ==  [{'complete': False, 'description': 'my first todo', 'id': 1, 'owner_id': 1,
                                "priority": 3, "title": "first todo"}]

