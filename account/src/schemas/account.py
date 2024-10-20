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
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    password: Optional[str] = None


class GetAccount(BaseModel):
    from_account:int 
    count:int


class UserResponse(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
    role: list[str]

    class Config:
        orm_mode = True 



class DoctorResponse(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
    role: list[str]
    specialty:str

    class Config:
        orm_mode = True 