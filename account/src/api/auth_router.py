from fastapi import APIRouter,Request
from fastapi.responses import Response

from .account_router import protected  
from ..schemas.auth import RegistrationUser, LoginUser

from loader import auth_utils
from loader import db



unprotected = APIRouter(prefix="/api")



@unprotected.post("/Authentication/SignUp")
async def sign_up(user_data:RegistrationUser, response:Response):
    if user_data:
        user = await db.get_user_by_username(user_data.username)
        if user:
            return "такой пользователь уже существует"
        
       
        id = auth_utils.create_user_id()
        access_token, refresh_token = auth_utils.create_access_token({"id":id, "role":"user"}), auth_utils.create_refresh_token({"id":id, "role":"user"})

        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)

        create_user = await db.create_user(id,user_data.username, user_data.firstName, user_data.lastName, user_data.password, refresh_token, "user")
       
        return "создан пользователь", create_user

    
    




@unprotected.post("/Authentication/Refresh")
async def refresh():
    pass



@unprotected.post("/Authentication/SignIn")
async def sign_in(user_data:LoginUser, response:Response):
 

    user = await db.get_user_by_username_and_password(user_data.username, user_data.password)
    print(user)
    if user:
        access_token, refresh_token = auth_utils.create_access_token({"id":user.id, "role":user.role}), auth_utils.create_refresh_token({"id":user.id, "role":user.role})
        await db.update_refresh_token(user.id, refresh_token)
        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)
        


        return "вы успешно вошли и токены были обновлены"
    return "что то не так"
    
  
             
             
             
             




    


@unprotected.put("/Authentication/SignOut")
async def sign_out(response: Response):
 
    response.delete_cookie(key="access_token",httponly=True)
    response.delete_cookie(key="refresh_token", httponly=True)

    return "токены удалены и вы вышли"


    



@unprotected.get("/Authentication/Validate")
async def validate():
    pass






