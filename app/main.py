import time

from fastapi import Depends, FastAPI
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.crud import create, delete, get_alll, read, update
from app.db import SessionLocal, engine
from app.models import Base
from app.schemas import CarSchema

app = FastAPI()

for i in range(5):
    try:
        Base.metadata.create_all(bind=engine)
        break
    except OperationalError:
        time.sleep(i + 1)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.post("/create")
async def create_car(schema: CarSchema, db: Session = Depends(get_db)):
    car = create(db, schema)

    if car is None:
        return {"message": "Car already exists"}
    else:
        return car


@app.get("/read/{id}")
async def read_car(id: int, db: Session = Depends(get_db)):
    car = read(db, id)

    if car is None:
        return {"message": "car not found"}
    else:
        return car


@app.post("/update")
async def update_car(schema: CarSchema, db: Session = Depends(get_db)):
    car = update(db, schema)

    if car is None:
        return {"message": "car not found"}
    else:
        return car


@app.post("/delete/{id}")
async def delete_car(id: int, db: Session = Depends(get_db)):
    car = delete(db, id)

    if car is None:
        return {"message": "Car not found"}
    else:
        return car


@app.get("/list")
async def get_all_cars(db: Session = Depends(get_db)):
    return get_alll(db)