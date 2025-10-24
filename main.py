import uvicorn
from fastapi import FastAPI
from todo.database import engine, Base
from todo.routers import todo_router, auth_router
# from todo.models


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(todo_router)
app.include_router(auth_router)

@app.get("/")
def get_root():
    return {"Hello": "Todos"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
