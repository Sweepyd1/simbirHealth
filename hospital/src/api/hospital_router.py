from fastapi import APIRouter, Request, Query, Depends,HTTPException
from fastapi.responses import Response
from ..database.models import Hospital
from typing import List
from loader import db
from uuid import uuid4
from ..schemas.hospitals import HospitalSchema
from ..utils.utils import get_current_user

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


@protected.post("/Hospitals")
async def create_hospital(request: Request, hospital_data: HospitalSchema, user = Depends(get_current_user)):
    if "admin" not in user["role"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    
    try:
        hospital = await db.create_new_hospital(
            hospital_data.name,
            hospital_data.address,
            hospital_data.phone,
            hospital_data.rating,
            hospital_data.email,
            hospital_data.city
        )
        await db.create_new_rooms(hospital.id, hospital_data.rooms)  # Assuming `hospital` has an `id` attribute
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


@protected.put("/Hospitals/{id}")
async def change_hospital_data(id: int, update_hospital_data: HospitalSchema, user = Depends(get_current_user)):
    if "admin" not in user["role"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    
    success = await db.update_hospital_data(id, update_hospital_data)
    if success:
        return {"status_code": 200, "detail": "Hospital data updated successfully."}
    else:
        raise HTTPException(status_code=404, detail="Hospital not found or data update failed.")


@protected.delete("/Hospitals/{id}")
async def delete_hospital(id: int, user = Depends(get_current_user)):
    if "admin" not in user["role"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    
    success = await db.delete_hospital(id)
    if success:
        return {"status_code": 204, "detail": "Hospital deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Hospital not found or deletion failed.")
    



