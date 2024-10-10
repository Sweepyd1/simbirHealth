from sqlalchemy import Column, Integer, BIGINT, TIMESTAMP, String, ForeignKey,Float
from datetime import datetime
from typing import Any

from .database import Base



class Hospital(Base):
    __tablename__ = 'hospitals'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    rating = Column(Float,  nullable=False)  
    email = Column(String,  nullable=False)  
    city = Column(String,  nullable=False)  


    def to_dict(self) -> dict[str, Any]:
        return{
            'id':self.id,
            'name':self.name,
            'address':self.address,
            'phone':self.phone,
            'rating':self.rating,
            'email':self.email,
            'city':self.city

        }
    

