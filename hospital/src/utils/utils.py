from fastapi import HTTPException
from fastapi import Request
import aiohttp
from datetime import datetime
from fastapi.responses import Response



async def get_current_user(request: Request, response: Response):
    access_token = request.cookies.get("access_token")
    
    try:
        # If access token exists, validate it
        if access_token:
            data = await validate_token(access_token=access_token)
            print(data)
            data = data["token_data"]

            # Check if the token is active
            if data["isActive"]:
                return data["user"]
                
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token:
            token = await update_token(refresh_token) 
             
            print(token["token"])

                # Set the new access token in the response cookies
            response.set_cookie(
                key="access_token",
                value=token["token"],
                httponly=True,
                expires=token["expires"],
                path="/",  # Убедитесь, что путь установлен корректно
                samesite='Lax',  # Если используется HTTPS, добавьте secure=True
                  # Если ваш сервер работает по HTTPS
            )
           

                
            # return await get_current_user(request=request, response=response)

    except Exception as e:
        print(f"Error validating or updating token: {e}")
    
    return None
        
async def update_token(refresh_token):
      async with aiohttp.ClientSession() as session:
        try:
            
            async with session.post("http://localhost:8080/api/Authentication/Refresh", json={"refresh_token":refresh_token}) as resp:
                if resp.status == 200:
                    # print("Tokens sent successfully")
                    # print(await resp.json())
                    return await resp.json()
                else:
                    print(f"Failed to send tokens: {resp.status}, Response: {await resp.text()}")
        except Exception as e:
            print(f"Error while sending tokens: {str(e)}")       





async def validate_token(access_token):
    async with aiohttp.ClientSession() as session:
        try:
            
            async with session.get("http://localhost:8080/api/Authentication/Validate", params={"accessToken": access_token}) as resp:
                if resp.status == 200:
                    # print("Tokens sent successfully")
                    return await resp.json()
                else:
                    print(f"Failed to send tokens: {resp.status}, Response: {await resp.text()}")
        except Exception as e:
            print(f"Error while sending tokens: {str(e)}")







    
