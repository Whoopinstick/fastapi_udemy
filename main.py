from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str | None = ""
    rating: int = Field(gt=0, le=5)



BOOKS = [Book(id=1, title="First Book", author="First Author", description="The First Book Written!", rating=5),
        Book(id=2, title="Second Book", author="Second Author", description="The Second Book Written!", rating=4),
        Book(id=3, title="Third Book", author="First Author", description="Another book", rating=3),
        Book(id=4, title="Fourth Book", author="Third Author", description="A book about cool stuff", rating=5)
         ]


@app.get("/books")
async def get_books():
    return BOOKS


@app.post("/books")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)
    return {"data": new_book}




if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)