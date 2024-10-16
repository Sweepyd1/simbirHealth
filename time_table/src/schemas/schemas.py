from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta

class TimetableEntry(BaseModel):
    
    hospitalId: int
    doctorId: int
    from_: datetime
    to: datetime
    room: str
    

    @validator('to')
    def check_time_difference(cls, to_time, values):
        from_time = values.get('from_')
        if from_time and (to_time - from_time) > timedelta(hours=12):
            raise ValueError("The difference between 'from' and 'to' must not exceed 12 hours.")
        return to_time

    @validator('from_')
    def check_time_multiple_of_30(cls, from_time):
        if from_time.minute % 30 != 0:
            raise ValueError("Minutes must be multiples of 30.")
        return from_time

    @validator('to')
    def check_to_multiple_of_30(cls, to_time):
        if to_time.minute % 30 != 0:
            raise ValueError("Minutes must be multiples of 30.")
        return to_time