import time
from fastapi import Depends, FastAPI
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.crud import create, delete, get_all, read, update
from app.schemas import CarSchema
from app.db import get_db

app = FastAPI()

for i in range(5):
    try:
        db = next(get_db())
        db.list_collection_names()
        break
    except ConnectionFailure:
        time.sleep(i + 1)


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.post("/create")
async def create_car(schema: CarSchema, db=Depends(get_db)):
    car = create(db, schema)
    if car is None:
        return {"message": "Car already exists"}
    return car


@app.get("/read/{id}")
async def read_car(id: str, db=Depends(get_db)):
    car = read(db, id)
    if car is None:
        return {"message": "Car not found"}
    return car


@app.put("/update")
async def update_car(id: str, schema: CarSchema, db=Depends(get_db)):
    car = update(db, id, schema)
    if car is None:
        return {"message": "Car not found"}
    return car


@app.delete("/delete/{id}")
async def delete_car(id: str, db=Depends(get_db)):
    car = delete(db, id)
    if car is None:
        return {"message": "Car not found"}
    return car


@app.get("/list")
async def get_all_cars(db=Depends(get_db)):
    return get_all(db)
