from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException, status
import uvicorn
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

class Book:
    def __init__(self, book_id: int, title: str, author: str, description: str, rating: int, published_year: int):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year


class BookRequest(BaseModel):
    book_id: Optional[int] = Field(description="System will auto-assign", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, le=5)
    published_year: int = Field(gt=0, le=datetime.now().year)

    # update the pydantic example
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "My New Book",
                "author": "Kevin Paul",
                "description": "My new book covers various topics",
                "rating": 5,
                "published_year": datetime.now().year
            }
        }
    }



BOOKS = [Book(book_id=1, title="First Book", author="First Author", description="The First Book Written!", rating=5,
              published_year=1990),
        Book(book_id=2, title="Second Book", author="Second Author", description="The Second Book Written!", rating=4,
             published_year=2000),
        Book(book_id=3, title="Third Book", author="First Author", description="Another book", rating=3,
             published_year=2023),
        Book(book_id=4, title="Fourth Book", author="Third Author", description="A book about cool stuff", rating=5,
             published_year=2010)
         ]

def get_next_book_id(book: Book):
    book.book_id = 1 if len(BOOKS) == 0 else BOOKS[-1].book_id + 1
    return book


# @app.get("/books")
# async def get_books():
#     return BOOKS

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books(book_rating: int = Query(gt=0, le=5, default=None,
                                             description="Leave blank for ALL, or filter for a value between 1 and 5 inclusive")
                    ,published_year: int = Query(gt=0, le=datetime.now().year, default=None,
                                                 description=f"Leave blank for ALL, or filter for a value between 0 and {datetime.now().year} inclusive")):
    books_to_return = []
    if not book_rating and not published_year:
        return BOOKS
    else:
        if book_rating and not published_year:
            for book in BOOKS:
                if book.rating == book_rating:
                    books_to_return.append(book)

        elif published_year and not book_rating:
            for book in BOOKS:
                if book.published_year == published_year:
                    books_to_return.append(book)

        else:
            for book in BOOKS:
                if book.rating == book_rating and book.published_year == published_year:
                    books_to_return.append(book)

    if len(books_to_return) > 0:
        return books_to_return
    else:
        raise HTTPException(status_code=404, detail="No books found")


@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.book_id == book_id:
            return book
    raise HTTPException(status_code=404, detail="No book found")


@app.post("/books",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(get_next_book_id(new_book))
    return {"data": new_book}


@app.put("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_book_by_id(book_request: BookRequest, book_id: int = Path(gt=0)):
    updated_book = Book(**book_request.model_dump())
    for book in BOOKS:
        if book.book_id == book_id:
            book.title = updated_book.title
            book.author = updated_book.author
            book.description = updated_book.description
            book.rating = updated_book.rating
        return book
    raise HTTPException(status_code=404,detail="No results found")

@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id: int = Path(gt=0)):
    for index, book in enumerate(BOOKS):
        if book.book_id == book_id:
            BOOKS.pop(index)
            return
    raise HTTPException(status_code=404, detail="No results found")

if __name__ == "__main__":
    uvicorn.run(app="example_001_fastapi_basics_with_validations:app", host="0.0.0.0", port=8002, reload=True)