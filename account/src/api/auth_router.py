from datetime import datetime
from fastapi import APIRouter,Request,Cookie
from fastapi.responses import Response

from .account_router import protected  
from ..schemas.auth import RegistrationUser, LoginUser

from loader import auth_utils
from loader import db

import aiohttp


unprotected = APIRouter(prefix="/api")



@unprotected.post("/Authentication/SignUp")
async def sign_up(user_data:RegistrationUser, response:Response):
    if user_data:
        user = await db.get_user_by_username(user_data.username)
        if user:
            return "такой пользователь уже существует"
        
        

        id = auth_utils.create_user_id()
        access_token = auth_utils.create_access_token({"id":id, "role":"user"})
        refresh_token = auth_utils.create_refresh_token({"id":id, "role":"user"})


  

        


        

       

        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)

        create_user = await db.create_user(id,user_data.username, user_data.firstName, user_data.lastName, user_data.password, refresh_token, "user")
       
        return "создан пользователь", create_user

    
    



#обновление токена
@unprotected.post("/Authentication/Refresh")
async def refresh(request:Request):
    print(request)
    # data = await request.json()
    # print(data)
    # access_token = data["access_token"]
    # print(access_token)
    # print(refresh_token)
    pass
    
    
    






@unprotected.post("/Authentication/SignIn")
async def sign_in(user_data:LoginUser, response:Response):
 

    user = await db.get_user_by_username_and_password(user_data.username, user_data.password)
    print(user)
  
    if user:
        
        access_token = auth_utils.create_access_token({"id":user.id, "role":user.role})
        refresh_token = auth_utils.create_refresh_token({"id":user.id, "role":user.role})

        await db.update_refresh_token(user.id, refresh_token)

        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post("http://localhost:8081/set_tokens", json={
                    "access_token": access_token,
                    "refresh_token":refresh_token
                }) as resp:
                    if resp.status == 200:
                        print("Tokens sent successfully")
                    else:
                        print(f"Failed to send tokens: {resp.status}")
            except Exception as e:
                print(f"Error while sending tokens: {str(e)}")

       




        


        return "вы успешно вошли и токены были обновлены"
    return "что то не так"
    
  
             
             
             
             




    


@unprotected.put("/Authentication/SignOut")
async def sign_out(response: Response):
 
    response.delete_cookie(key="access_token",httponly=True)
    response.delete_cookie(key="refresh_token", httponly=True)

    return "токены удалены и вы вышли"


    



@unprotected.get("/Authentication/Validate")
async def validate(request:Request):

    data = await request.json()
    access_token = data["access_token"]


    user = auth_utils.decode_token(access_token)
    print(user)

    return user



   



    






