from fastapi import APIRouter, Request, Query, Depends,HTTPException
from fastapi.responses import Response
from ..database.models import Hospital
from typing import List
from loader import db
from uuid import uuid4
from ..schemas.hospitals import HospitalSchema
from ..utils.utils import get_current_user, update_token
from ..utils.change_data import delete_all_record_with_hospital, change_all_record_with_hospital

import aiohttp

protected = APIRouter(prefix="/api", tags=["сервис больниц"])

@protected.get("/Hospitals")
async def get_hospitals(request: Request, from_: int = Query(0), count: int = Query(10), user = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated.")
    try:
        result = await db.get_all_hospital(from_, count)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected.get("/Hospitals/{id}")
async def get_hospitals_by_id(hospital_id: int, user = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated.")
    hospital = await db.get_hospital_by_id(hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found.")
    return hospital

###!!!!!!!!!!!!!!!!!!!!!!!!!

@protected.post("/Hospitals")
async def create_hospital(request: Request,response:Response, hospital_data: HospitalSchema, user = Depends(get_current_user)):

    if user["status"] != "authentication":
        response.set_cookie("access_token",user["token"])
        user = get_current_user(request)
        
        
    if "admin" not in user["role"] or user is None:
        raise HTTPException(status_code=403, detail="Access denied.")
        
    if len(hospital_data.rooms) != len(set(hospital_data.rooms)):
        raise HTTPException(status_code=400, detail="Room names must be unique.")
    try:
        hospital = await db.create_new_hospital(
            hospital_data.name,
            hospital_data.address,
            hospital_data.phone,
            hospital_data.rating,
            hospital_data.email,
            hospital_data.city,
            
        )
        await db.create_new_rooms(hospital.id, hospital_data.rooms)  
        return {"status_code": 201, "detail": "Hospital created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected.get("/Hospitals/{id}/Rooms")
async def get_rooms_in_hospital(id_hospital: int, user = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated.")
    
    try:
        result = await db.get_rooms_in_hospital_by_id(id_hospital)
        if not result:
            raise HTTPException(status_code=404, detail="Rooms not found in this hospital.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#####send another server that change
@protected.put("/Hospitals/{id}")
async def change_hospital_data(id: int, update_hospital_data: HospitalSchema, user = Depends(get_current_user)):
    if "admin" not in user["role"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    
    success = await db.update_hospital_data(id, update_hospital_data)
  
    if success["is_correct"]:
        # print(success["old_rooms"])
        result = await change_all_record_with_hospital(id,update_hospital_data.rooms, success["old_rooms"])
        print(result)
        return {"status_code": 200, "detail": "Hospital data updated successfully."}
    else:
        raise HTTPException(status_code=404, detail="Hospital not found or data update failed.")

#####delete any record in other servers
@protected.delete("/Hospitals/{id}")
async def delete_hospital(id: int, user = Depends(get_current_user)):
    if "admin" not in user["role"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    
    success = await db.delete_hospital(id)
    if success:
        result = await delete_all_record_with_hospital(id)
        return {"status_code": 204, "detail": "Hospital deleted successfully.", "result":result}
    else:
        raise HTTPException(status_code=404, detail="Hospital not found or deletion failed.")
    



@protected.post("/test")
async def post(response:Response):
    token = await update_token()
    response.set_cookie("gruergbhiergb",token)
