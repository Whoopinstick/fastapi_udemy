from typing import Optional

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    def __init__(self, book_id: int, title: str, author: str, description: str, rating: int):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    book_id: Optional[int] = Field(description="System will auto-assign", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, le=5)

    # update the pydantic example
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "My New Book",
                "author": "Kevin Paul",
                "description": "My new book covers various topics",
                "rating": 5
            }
        }
    }



BOOKS = [Book(book_id=1, title="First Book", author="First Author", description="The First Book Written!", rating=5),
        Book(book_id=2, title="Second Book", author="Second Author", description="The Second Book Written!", rating=4),
        Book(book_id=3, title="Third Book", author="First Author", description="Another book", rating=3),
        Book(book_id=4, title="Fourth Book", author="Third Author", description="A book about cool stuff", rating=5)
         ]

def get_next_book_id(book: Book):
    book.book_id = 1 if len(BOOKS) == 0 else BOOKS[-1].book_id + 1
    return book


# @app.get("/books")
# async def get_books():
#     return BOOKS

@app.get("/books")
async def get_books(book_rating: int = -1):
    books_to_return = []
    if book_rating == -1:
        return BOOKS
    else:
        for book in BOOKS:
            if book.rating == book_rating:
                books_to_return.append(book)
        return books_to_return


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    for book in BOOKS:
        if book.book_id == book_id:
            return book
    return "No results found"


@app.post("/books")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    # BOOKS.append(new_book)
    BOOKS.append(get_next_book_id(new_book))
    return {"data": new_book}


@app.put("/books/{book_id}")
async def update_book_by_id(book_id: int, book_request: BookRequest):
    updated_book = Book(**book_request.model_dump())
    for book in BOOKS:
        if book.book_id == book_id:
            book.title = updated_book.title
            book.author = updated_book.author
            book.description = updated_book.description
            book.rating = updated_book.rating
        return book
    return "No results found"

@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int):
    for index, book in enumerate(BOOKS):
        if book.book_id == book_id:
            BOOKS.pop(index)
            break

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)