from fastapi import FastAPI
import uvicorn

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get("/")
async def get_root():
    return "Hello, World"

@app.get("/greeting/{user}")
async def greet_user(user: str):
    return {"data": f"Hello, {user}"}

@app.get("/books")
async def get_books():
    return BOOKS

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    return BOOKS[book_id]

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)