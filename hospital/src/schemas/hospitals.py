from pydantic import BaseModel

class HospitalSchema(BaseModel):
    name: str
    address: str
    phone: str
    rating: float
    email: str
    city: str
    rooms: list