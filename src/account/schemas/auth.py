from pydantic import BaseModel

class AccessToken(BaseModel):
    access_token:str


class LoginUser(BaseModel):
    username:str 
    password:str 


class RefreshToken(BaseModel):
    access_token:str


class RegistrationUser(BaseModel):
    lastName:str 
    firstName:str 
    username:str 
    password:str 
   