from typing import Optional
from pydantic import BaseModel
from dataclasses import dataclass
from ..database.models import User
from datetime import datetime

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


@dataclass
class IsAuthenticated():
    is_authenticated:bool
    user:Optional[User]
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    token:str 
    isActive:bool
    user:dict