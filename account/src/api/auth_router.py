from datetime import datetime, timedelta
from fastapi import APIRouter,Request,Cookie, HTTPException, Query
from fastapi.responses import Response

from .account_router import protected  
from ..schemas.auth import RegistrationUser, LoginUser, TokenData

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

        access_exp = auth_utils.decode_token(access_token)["exp"]
        refresh_exp = auth_utils.decode_token(refresh_token)["exp"]

        access_exp_str = datetime.utcfromtimestamp(access_exp).strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        refresh_exp_str = datetime.utcfromtimestamp(refresh_exp).strftime("%a, %d-%b-%Y %H:%M:%S GMT")


  

        


        

       

        response.set_cookie("access_token", access_token, httponly=True, expires=access_exp_str)
        response.set_cookie("refresh_token", refresh_token, httponly=True, expires=refresh_exp_str)

        create_user = await db.create_user(id,user_data.username, user_data.firstName, user_data.lastName, user_data.password, refresh_token, "user")
       
        return "создан пользователь", create_user

    
    





    
    
    






@unprotected.post("/Authentication/SignIn")
async def sign_in(user_data:LoginUser, response:Response):
 

    user = await db.get_user_by_username_and_password(user_data.username, user_data.password)
    print(user)
  
    if user:
        
        access_token = auth_utils.create_access_token({"id":user.id, "role":user.role})
        refresh_token = auth_utils.create_refresh_token({"id":user.id, "role":user.role})

        access_exp = auth_utils.decode_token(access_token)["exp"]
        refresh_exp = auth_utils.decode_token(refresh_token)["exp"]

        access_exp_str = datetime.utcfromtimestamp(access_exp).strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        refresh_exp_str = datetime.utcfromtimestamp(refresh_exp).strftime("%a, %d-%b-%Y %H:%M:%S GMT")

       

        await db.update_refresh_token(user.id, refresh_token)
       

        response.set_cookie("access_token", access_token, httponly=True, expires=access_exp_str)
        response.set_cookie("refresh_token", refresh_token, httponly=True, expires=refresh_exp_str)

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


                async with session.post("http://localhost:8082/set_tokens", json={
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
async def validate(accessToken: str = Query(...)):
    user = auth_utils.decode_token(accessToken)
    print(user)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    
    expiration_time = datetime.fromtimestamp(user.get("exp")) 
    current_time = datetime.utcnow()

    is_active = current_time < expiration_time 

    token_data = TokenData(
        token=accessToken,
        isActive=is_active,
        user=user  
    )
    
    return token_data


   


@unprotected.post("/Authentication/Refresh")
async def refresh(request:Request, response:Response):

    data = await request.json()
    refresh_token = data["refresh_token"]
    

    payload = auth_utils.decode_token(refresh_token)

    new_access_token = auth_utils.create_access_token(payload)
  

    access_exp = auth_utils.decode_token(new_access_token)["exp"]

 

    access_exp_str = datetime.utcfromtimestamp(access_exp).strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie(
        "access_token",
        new_access_token,
        httponly=True,
        expires=access_exp_str,
        path="/",
        samesite='None'  # Set to root path to make it accessible site-wide
          # Adjust if necessary
    )
    print("ткоен установлен")
      


    async with aiohttp.ClientSession() as session:
            try:
    #         #     async with session.post("http://localhost:8081/set_tokens", json={
    #         #         "access_token": new_access_token,
                   
    #         #     }) as resp:
    #         #         if resp.status == 200:
    #         #             print("Tokens sent successfully")
    #         #         else:
    #         #             print(f"Failed to send tokens: {resp.status}")
    #         # except Exception as e:
    #         #     print(f"Error while sending tokens: {str(e)}")


                async with session.post("http://localhost:8082/set_tokens", json={
                    "data": {"token":new_access_token, "expires":access_exp_str},
                   
                }) as resp:
                    if resp.status == 200:
                        print("Tokens sent successfully")
                    else:
                        print(f"Failed to send tokens: {resp.status}")
            except Exception as e:
                print(f"Error while sending tokens: {str(e)}")





    
    






