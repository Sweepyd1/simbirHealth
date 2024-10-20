from sqlalchemy import Column, Integer, BIGINT, TIMESTAMP, String, ForeignKey, DateTime
from datetime import datetime
from typing import Any

from .database import Base



class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, nullable=False,primary_key=True)
    date = Column(DateTime(timezone=False), nullable=False)
    pacient_id = Column(Integer, nullable=False)
    hospital_id = Column(Integer, nullable=False )
    doctor_id = Column(Integer, nullable=False)


    room  = Column(String, nullable=False )
    data = Column(String, nullable=True)



    def to_dict(self) -> dict[str, Any]:
        return{
            'id':self.id,
            'date':self.date,
            'pacient_id':self.pacient_id,
            'hospital_id':self.hospital_id,
            'doctor_id':self.doctor_id,
            'room':self.room,
            'data':self.data

        }
    

