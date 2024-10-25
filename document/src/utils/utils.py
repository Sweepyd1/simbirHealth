from fastapi import HTTPException
from fastapi import Request
import aiohttp
from datetime import datetime
from fastapi.responses import Response

from config import ACCOUNT_SERVER_URL, DOCUMENT_SERVICE_TOKEN

async def get_current_user(request: Request, response: Response):
    access_token = request.cookies.get("access_token")
    
    try:
        if access_token:
            data = await validate_token(access_token=access_token)
            data = data["token_data"]

            if data["isActive"]:
                return data["user"]

        refresh_token = request.cookies.get("refresh_token")
        if refresh_token:
            token = await update_token(refresh_token) 
            print("Token updated:", token)

            response.set_cookie(
                    key="access_token",
                    value=token["data"]["token"], 
                    httponly=True,
                    expires=token["data"]["expires"]
                )
            return await get_current_user(request=request, response=response)

    except Exception as e:
        print(f"Error validating or updating token: {e}")
    
    return None
        

        
        
       





async def validate_token(access_token):
    async with aiohttp.ClientSession() as session:
        try:
            
            async with session.get(f"{ACCOUNT_SERVER_URL}/api/Authentication/Validate", params={"accessToken": access_token, "service_token":DOCUMENT_SERVICE_TOKEN}) as resp:
                if resp.status == 200:
                    print("Tokens sent successfully")
                    return await resp.json()
                else:
                    print(f"Failed to send tokens: {resp.status}, Response: {await resp.text()}")
        except Exception as e:
            print(f"Error while sending tokens: {str(e)}")


async def update_token(refresh_token):
      async with aiohttp.ClientSession() as session:
        try:
            
            async with session.post(f"{ACCOUNT_SERVER_URL}/api/Authentication/Refresh", json={"refresh_token":refresh_token,"service_token":DOCUMENT_SERVICE_TOKEN}) as resp:
                if resp.status == 200:
                    print("Tokens sent successfully")
                    return await resp.json()
                else:
                    print(f"Failed to send tokens: {resp.status}, Response: {await resp.text()}")
        except Exception as e:
            print(f"Error while sending tokens: {str(e)}")




    
