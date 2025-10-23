import uvicorn
from fastapi import FastAPI
from todo.database import engine, Base
from todo.routers import auth, todos


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)

@app.get("/")
def get_root():
    return {"Hello": "Todos"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
