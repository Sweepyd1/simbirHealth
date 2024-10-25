from sqlalchemy import Column, Integer, BIGINT, TIMESTAMP, String, ForeignKey,Float
from datetime import datetime
from typing import Any, Dict
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import ARRAY

from .database import Base




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False )
    lastName  = Column(String, nullable=False )
    firstName  = Column(String, nullable=False)
    password  = Column(String, nullable=False )
    refresh_token = Column(String, nullable=True)
    role = Column(ARRAY(String), nullable=False)

    def to_dict(self) -> dict[str, Any]:
        return{
            'id':self.id,
            'username':self.username,
            'lastName':self.lastName,
            'firstName':self.firstName,
            'password':self.password,
            'refresh_token':self.refresh_token,
            'role':self.role

        }


class Doctor(User):
    __tablename__ = "doctors"
    id = Column(Integer, ForeignKey('users.id',ondelete='CASCADE'), primary_key=True)  
    specialty = Column(String, nullable=False)
    user = relationship("User", backref="doctor_details")

    def to_dict(self) -> dict[str, Any]:
        user_dict = super().to_dict()  
        user_dict['specialty'] = self.specialty  
        return user_dict


