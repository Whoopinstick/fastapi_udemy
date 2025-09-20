# example 1
# local data in a list
# basic path and query parameters

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


class Book(BaseModel):
    title: str
    author: str
    category: str



@app.get("/")
async def get_root():
    return "Hello, World"

@app.get("/greeting/{user}")
async def greet_user(user: str):
    return {"data": f"Hello, {user}"}

@app.get("/books")
async def get_books(category: str = "all"):
    if category.lower() == "all":
        return BOOKS
    else:
        books_to_return = []
        for book in BOOKS:
            if category.lower() == book["category"].lower():
                books_to_return.append(book)

        if not books_to_return:
            return "no results"
        else:
            return books_to_return

@app.get("/books/{book_title}")
async def get_book_by_title(book_title: str, category: str = "all"):
    if category.lower() == "all":
        for book in BOOKS:
            if book_title.lower() == book["title"].lower():
                return book
            else:
                return "no results"
    else:
        for book in BOOKS:
            if book_title.lower() == book["title"].lower() and category.lower() == book["category"].lower():
                return book
            else:
                return "no results"

    return "no results"


# as a query parameter, instead of POSTing to body
@app.post("/books")
async def insert_book(title: str, author: str, category: str):
    new_book = {"title": title, "author": author, "category": category}
    BOOKS.append(new_book)
    return new_book

# post to a request body
@app.post("/books2")
async def insert_book(new_book: Book):
    book_to_insert = {"title": new_book.title, "author": new_book.author, "category": new_book.category}
    BOOKS.append(book_to_insert)
    return new_book

@app.put("/books/{book_title}")
async def update_book(book_title: str, updated_book: Book):
    for book in BOOKS:
        if book_title.lower() == book["title"].lower():
            book["title"] = updated_book.title
            book["author"] = updated_book.author
            book["category"] = updated_book.category
            return book
        else:
            continue
    return "no results"

@app.delete("/books/{book_title}")
async def delete_book(book_title: str):
    for book in BOOKS:
        if book_title.lower() == book["title"].lower():
            BOOKS.remove(book)
            return "book deleted"

    return "no results"


if __name__ == "__main__":
    uvicorn.run(app="example_001_fastapi_basics:app", host="0.0.0.0", port=8001, reload=True)