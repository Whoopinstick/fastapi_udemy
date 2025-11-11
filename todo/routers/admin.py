from fastapi import APIRouter, status, HTTPException, Depends, Path
from todo.database import get_db
from typing import Annotated
from todo.models import Todos
from sqlalchemy.orm import Session
from todo.oath2 import get_current_user

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/todos", status_code=status.HTTP_200_OK)
async def admin_get_all_todos(db: db_dependency, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    return db.query(Todos).all()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        db.delete(todo_model)
        db.commit()