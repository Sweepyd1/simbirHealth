from fastapi import APIRouter

from loader import db
unprotected = APIRouter(prefix="/api")

from .account_router import protected  
from ..schemas.auth import RegistrationUser


@unprotected.post("/Authentication/SignUp")
async def sign_up(user_data:RegistrationUser):
    if user_data:

        await db.create_user(user_data.username, user_data.firstName, user_data.lastName, user_data.password)
    
    




@unprotected.post("/Authentication/Refresh")
async def refresh():
    pass



@unprotected.post("/Authentication/SignIn")
async def sign_in():
    pass


@protected.put("/Authentication/SignOut")
async def sign_out():
    pass



@unprotected.get("/Authentication/Validate")
async def validate():
    pass






