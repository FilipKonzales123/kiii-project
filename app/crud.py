from sqlalchemy.orm import Session
from . import models, schemas


def read(db: Session, id: int):
    return db.query(models.Car).filter(models.Car.id == id).first()

def create(db: Session, schema: schemas.CarSchema):
    find_car = read(db, schema.id)
    if find_car is not None:
        return None
    car = models.Car(
        id=schema.id,
        brand=schema.brand,
        model=schema.model,
        year=schema.year
    )
    db.add(car)
    db.commit()
    db.refresh(car)
    return car

def update(db: Session, schema: schemas.CarSchema):
    car = read(db, schema.id)
    if car is None:
        return None
    car.brand = schema.brand
    car.model = schema.model
    car.year = schema.year

    db.commit()
    db.refresh(car)
    return car
    
def delete(db: Session, id: int):
    car = read(db, id)
    db.delete(car)
    db.commit()
    return car

def get_alll(db: Session):
    return db.query(models.Car).all()