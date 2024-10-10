from fastapi import APIRouter, Request, Query
from fastapi.responses import Response
from ..database.models import Hospital
from typing import List
# from ..utils.ProtectedRouter import protected


protected = APIRouter(prefix="/api", tags=["сервис больниц"])
from loader import db
from uuid import uuid4
from ..schemas.hospitals import HospitalSchema
import aiohttp



async def get_user(access_token):
    async with aiohttp.ClientSession() as session:
            try:
                async with session.get("http://localhost:8080/api/Authentication/Validate", json={
                    "access_token": access_token,
                 
                    
                }) as resp:
                    if resp.status == 200:
                        print("Tokens sent successfully")
                        return await resp.json()
                        
                    else:
                        print(f"Failed to send tokens: {resp.status}")
            except Exception as e:
                print(f"Error while sending tokens: {str(e)}")


@protected.get("/Hospitals")
async def get_hospitals(request:Request,from_: int = Query(), count: int = Query()):
    access_token = request.cookies.get("access_token")
    user = await get_user(access_token)
    if user:
        print(user)

    
  
    

        result = await db.get_all_hospital(from_, count)
        return result
    


@protected.get("/Hospitals/{id}")
async def get_hospitals_by_id(hospital_id: int = Query()):

    result = await db.get_hospital_by_id(hospital_id)
    return result


@protected.get("/Hospitals/{id}/Rooms")
async def get_rooms_in_hospital(id):
    pass


@protected.post("/Hospitals")
async def create_hospital(request:Request,hospital_data:HospitalSchema):
    access_token = request.cookies.get("access_token")
    user = await get_user(access_token=access_token)
    if user["role"] != "admin":
        return "нет прав"
    
    await db.create_new_hospital(hospital_data.id,hospital_data.name,hospital_data.address,hospital_data.phone,hospital_data.rating,hospital_data.email,hospital_data.city)
    return "создано успешно"



@protected.put("/Hospitals/{id}")
async def change_hospital(id):
    pass


@protected.put("/Hospitals/{id}")
async def delete_hospital(id):
    pass



