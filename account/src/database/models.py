from sqlalchemy import Column, Integer, BIGINT, TIMESTAMP, String, ForeignKey
from datetime import datetime
from typing import Any


from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String, nullable=False, primary_key=True)
    username = Column(String, nullable=False )
    lastName  = Column(String, nullable=False )
    firstName  = Column(String, nullable=False)
    password  = Column(String, nullable=False )
    refresh_token = Column(String, nullable=False)
    role = Column(String, nullable=False)



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
    

