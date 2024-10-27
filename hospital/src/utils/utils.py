from fastapi import HTTPException
from fastapi import Request
import aiohttp
from datetime import datetime
from fastapi.responses import Response
from config import ACCOUNT_SERVER_URL, HOSPITAL_SERVICE_TOKEN


async def get_current_user(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")
    try:
        if access_token and refresh_token:
            data = await validate_token(access_token=access_token)
            print(data)
            data = data["token_data"]
            if data["isActive"]:
                return data["user"]
                
        
        if refresh_token:
            token = await update_token(refresh_token) 
            print(token)
            
            return {"token":token, "status":False}
    except Exception as e:
        print(f"Error validating or updating token: {e}")
    
  
        
async def update_token(refresh_token):#refresh_token
    
    async with aiohttp.ClientSession() as session:
        try:
            
            async with session.post(f"{ACCOUNT_SERVER_URL}/api/Authentication/Refresh", json={"refresh_token":refresh_token, "service_token":HOSPITAL_SERVICE_TOKEN}) as resp:
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
            
            async with session.get(f"{ACCOUNT_SERVER_URL}/api/Authentication/Validate", params={"accessToken": access_token,"service_token":HOSPITAL_SERVICE_TOKEN}) as resp:
                if resp.status == 200:
                    # print("Tokens sent successfully")
                    return await resp.json()
                else:
                    print(f"Failed to send tokens: {resp.status}, Response: {await resp.text()}")
        except Exception as e:
            print(f"Error while sending tokens: {str(e)}")






    
