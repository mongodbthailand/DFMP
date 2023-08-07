from fastapi import FastAPI, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder

from typing import List
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from models import Book, BookUpdate
from bson.objectid import ObjectId
import os

app = FastAPI(title="DFMP API")

@app.on_event("startup")
def startup_db_client():
    uri = os.getenv('ATLAS_URI')
    if uri is None:
        uri = "mongodb://localhost:27017"
    try:
        app.mongodb = MongoClient(uri, server_api=ServerApi('1'))
        app.db = app.mongodb["test"]
        print("Connected!")
    except Exception as e:
        print(e)


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb.close()


@app.get("/", description="Hello World")
async def root():
    return {"message": "Hello World"}


@app.post("/create",  status_code=status.HTTP_201_CREATED, description="Create a new book", response_model=Book)
async def create(request: Request, book: Book = Body(...)):
    book = jsonable_encoder(book)
    print(book)
    new_book = request.app.db["books"].insert_one(book)
    created_book = request.app.db["books"].find_one(
        {"_id": new_book.inserted_id}
    )
    return created_book


@app.get("/read", description="Read all books", response_model=List[Book])
async def read(request: Request):
    books = list(request.app.db["books"].find(limit=100))
    return books


@app.put("/update/{bookId}", description="Update a book", response_model=Book)
async def update(id: str, request: Request, book: BookUpdate = Body(...)):
    book = {k: v for k, v in book.model_dump().items() if v is not None}
    if len(book) >= 1:
        updated_book = request.app.db["books"].find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": book})
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No book with this id: {id} found')
    return updated_book


@app.delete("/delete/{bookId}")
async def delete(id: str, request: Request, response: Response):
    delete_result = request.app.db["books"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Book with ID {id} not found")
