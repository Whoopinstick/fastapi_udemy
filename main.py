import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from todo.database import engine, Base
from todo.routers import todo_router, auth_router, admin_router, user_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(todo_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def get_root():
    # return {"Hello": "Todos"}
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/template_test")
def template_test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
