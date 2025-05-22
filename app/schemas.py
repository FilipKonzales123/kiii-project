from pydantic import BaseModel

class CarSchema(BaseModel):
    id: int
    brand: str
    model: str
    year: int