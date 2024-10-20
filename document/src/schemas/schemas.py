from pydantic import BaseModel
from datetime import datetime


class HistorySchemas(BaseModel):
    date:datetime
    pacient_id:int 
    hospital_id:int 
    doctor_id:int 
    room:str
    data:str
    