from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.getenv('ATLAS_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!!")
except Exception as e:
    print(e)

app = FastAPI()

@app.get("/", description="ROOT")
async def root():
    return {"message": "Hello World"}

@app.get("/create", description="Create a new book")
async def create():
    return {"message": "Hello Python"}

@app.post("/read")
async def read():
    return {"message": "Hello Python"}

@app.post("/update")
async def update():
    return {"message": "Hello Python"}

@app.post("/delete")
async def delete():
    return {"message": "Hello Python"}