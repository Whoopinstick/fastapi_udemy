import uvicorn
from fastapi import FastAPI, Request
from todo.database import engine, Base
from todo.routers import todo_router, auth_router, admin_router, user_router
from fastapi.templating import Jinja2Templates

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.include_router(todo_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)

@app.get("/")
def get_root():
    return {"Hello": "Todos"}

@app.get("/template_test")
def template_test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
