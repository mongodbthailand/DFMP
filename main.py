from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/create")
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