from sqlalchemy import Column, Integer, BIGINT, TIMESTAMP, String, ForeignKey
from datetime import datetime
from typing import Any

from .database import Base



class User(Base):
    __tablename__ = 'users'
    username = Column(String, nullable=False,primary_key=True )
    lastName  = Column(String, nullable=False )
    firstName  = Column(String, nullable=False)
    password  = Column(String, nullable=False )



    def to_dict(self) -> dict[str, Any]:
        return{
            'username':self.username,
            'lastName':self.lastName,
            'firstName':self.firstName,
            'password':self.password

        }
    

