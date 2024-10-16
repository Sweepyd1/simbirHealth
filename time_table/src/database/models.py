from sqlalchemy import Column, DateTime, Integer, BIGINT, TIMESTAMP, String, ForeignKey
from datetime import datetime
from typing import Any
from sqlalchemy.orm import relationship
from .database import Base



class TimeTable(Base):
    __tablename__ = 'time_table'
    
    id = Column(Integer, nullable=False, primary_key=True)
    hospitalId = Column(Integer, nullable=False)
    doctorId = Column(Integer, nullable=False)
    from_ = Column(DateTime(timezone=False), nullable=False)  
    to = Column(DateTime(timezone=False), nullable=False)
    room = Column(String, nullable=False) 
    
    butchured_times = relationship(
        "Butchured_time_table",
        order_by="Butchured_time_table.id",
        back_populates="time_table",
        cascade="all, delete-orphan"  # Устанавливаем каскадное удаление
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'hospitalId': self.hospitalId,
            'doctorId': self.doctorId,
            'from': self.from_.isoformat(),  
            'to': self.to.isoformat(),
        }

class Butchured_time_table(Base):
     __tablename__ = 'butcured_time_table'
     
     id = Column(Integer, nullable=False, primary_key=True)
     id_time_table = Column(Integer, ForeignKey('time_table.id',ondelete='CASCADE'), nullable=False)
     from_ = Column(DateTime(timezone=False), nullable=False)  
     to = Column(DateTime(timezone=False), nullable=False)
     enrolled_user_id = Column(Integer, nullable=True)

     time_table = relationship("TimeTable", back_populates="butchured_times")
     
     def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'id_time_table': self.id_time_table,
            'from': self.from_.isoformat(),  
            'to': self.to.isoformat(),
            'enrolled_user_id': self.enrolled_user_id,
        }

TimeTable.butchured_times = relationship("Butchured_time_table", order_by=Butchured_time_table.id, back_populates="time_table")