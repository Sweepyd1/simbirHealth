from sqlalchemy import Column, Integer, BIGINT, TIMESTAMP, String, ForeignKey,Float
from datetime import datetime
from typing import Any
from sqlalchemy.orm import relationship
from .database import Base



class Hospital(Base):
    __tablename__ = 'hospitals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    rating = Column(Float,  nullable=False)  
    email = Column(String,  nullable=False)  
    city = Column(String,  nullable=False)

    rooms = relationship("Room", back_populates="hospital", cascade="all, delete-orphan")  


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
    

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hospital_id = Column(Integer, ForeignKey('hospitals.id', ondelete='CASCADE'), nullable=False)  # Add ondelete='CASCADE'
    
    hospital = relationship("Hospital", back_populates="rooms")


    def to_dict(self) -> dict[str, Any]:
        return {
            'id':self.id,
            'name':self.name,
            'hospital_id':self.hospital_id,
            
        }
