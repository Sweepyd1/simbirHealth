from pydantic import BaseModel

class HospitalSchema(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    rating: float
    email: str
    city: str