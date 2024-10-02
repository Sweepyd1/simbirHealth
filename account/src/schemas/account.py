from pydantic import BaseModel
from typing import Optional


class DoctorFilterParams(BaseModel):
    nameFilter: Optional[str] = None 
    from_: int = 0  
    count: int = 10


class ChangeAccount(BaseModel):
    lastName:str
    firstName:str 
    username:str
    password:str
    roles:list[str]




class CreateAccount(BaseModel):
    lastName:str
    firstName:str 
    username:str
    password:str
    roles:list[str]



class UpdateAccount(BaseModel):
    lastName:str
    firstName:str 
    password:str


class GetAccount(BaseModel):
    from_account:int 
    count:int