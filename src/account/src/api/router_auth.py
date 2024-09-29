from fastapi import APIRouter


unprotected = APIRouter(prefix="/api")

from .account_router import protected  



@unprotected.post("/Authentication/SignUp")
async def sign_up():
    pass




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






