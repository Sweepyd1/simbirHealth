from sqlalchemy import Column, Integer, BIGINT, TIMESTAMP, String, ForeignKey,Float
from datetime import datetime
from typing import Any, Dict
from sqlalchemy.orm import relationship



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


class Doctor(User):
    __tablename__ = "doctors"

    id = Column(String, ForeignKey('users.id'), primary_key=True)  # Убедитесь, что id является первичным ключом

    specialty = Column(String, nullable=False)

  
    user = relationship("User", backref="doctor_details")


    def to_dict(self) -> dict[str, Any]:
        user_dict = super().to_dict()  
        user_dict['specialty'] = self.specialty  
        return user_dict

    

# class Hospital(Base):
#     __tablename__ = 'hospitals'

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     address = Column(String, nullable=False)
#     phone = Column(String, nullable=False)
#     rating = Column(Float,  nullable=False)  
#     email = Column(String,  nullable=False)  
#     city = Column(String,  nullable=False)  


#     def to_dict(self) -> dict[str, Any]:
#         return{
#             'id':self.id,
#             'name':self.name,
#             'address':self.address,
#             'phone':self.phone,
#             'rating':self.rating,
#             'email':self.email,
#             'city':self.city

#         }
    
