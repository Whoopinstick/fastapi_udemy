from fastapi import APIRouter, status, Path, HTTPException, Depends
from todo.database import get_db
from typing import Annotated
from todo.models import Todos
from todo.schemas import TodoRequest
from sqlalchemy.orm import Session

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter()

@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency):
    return db.query(Todos).all()

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        return todo_model

@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo: TodoRequest):
    new_todo_model = Todos(**todo.model_dump())
    db.add(new_todo_model)
    db.commit()

@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        todo_model.title =  todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.complete = todo.complete
        db.add(todo_model)
        db.commit()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        db.delete(todo_model)
        db.commit()