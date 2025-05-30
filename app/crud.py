from pymongo.database import Database
from bson.objectid import ObjectId
from .schemas import CarSchema

def serialize(doc):
    """Convert MongoDB's _id to string for JSON serialization."""
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

def read(db: Database, car_id: str):
    """Read a car by its MongoDB _id."""
    try:
        return serialize(db.cars.find_one({"_id": ObjectId(car_id)}))
    except:
        return None

def create(db: Database, schema: CarSchema):
    car_dict = schema.model_dump()
    result = db.cars.insert_one(car_dict)
    return serialize(db.cars.find_one({"_id": result.inserted_id}))

def update(db: Database, car_id: str, schema: CarSchema):
    """Update a car by its _id."""
    try:
        updated = db.cars.find_one_and_update(
            {"_id": ObjectId(car_id)},
            {"$set": schema.model_dump()},
            return_document=True
        )
        return serialize(updated)
    except:
        return None

def delete(db: Database, car_id: str):
    """Delete a car by its _id."""
    try:
        car = read(db, car_id)
        if car:
            db.cars.delete_one({"_id": ObjectId(car_id)})
        return car
    except:
        return None

def get_all(db: Database):
    """Get all cars."""
    return [serialize(doc) for doc in db.cars.find()]
