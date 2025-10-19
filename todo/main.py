from fastapi import FastAPI, Depends, HTTPException, Path, status
from typing import Annotated
import uvicorn
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Todos
from schemas import TodoRequest

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
app = FastAPI()

@app.get("/")
def get_root():
    return {"Hello": "Todos"}

@app.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency):
    return db.query(Todos).all()

@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        return todo_model

@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo: TodoRequest):
    new_todo_model = Todos(**todo.model_dump())
    db.add(new_todo_model)
    db.commit()

@app.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
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

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        db.delete(todo_model)
        db.commit()

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
