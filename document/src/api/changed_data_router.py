# from document_router import protected
from fastapi import Request, APIRouter, Request, HTTPException
from loader import db
from config import list_available_tokens

change_data = APIRouter(prefix="/api", tags=["изменение и синхронизация данных"])




##check token
@change_data.post("/delete_all_record/{hospital_id}")
async def delete_all_hospital_record_by_id(request:Request,hospital_id:int):
    data = await request.json()
    service_token = data["service_token"]
    if service_token not in list_available_tokens:
        raise HTTPException(status_code=403, detail="access denied")
    result = await db.delete_history_for_hospital(hospital_id)
    return result




##check token
@change_data.post("/change_all_record/{hospital_id}")
async def change_all_hospital_record_by_id(request:Request,hospital_id:int):
    data = await request.json()
    service_token = data["service_token"]
    if service_token not in list_available_tokens:
        raise HTTPException(status_code=403, detail="access denied")
    pass



##check token
@change_data.post("/delete_all_record_doctor/{doctor_id}")
async def delete_all_record_doctor(request:Request,doctor_id:int):
    data = await request.json()
    service_token = data["service_token"]
    if service_token not in list_available_tokens:
        raise HTTPException(status_code=403, detail="access denied")

    result = await db.delete_all_record_for_doctor(doctor_id)

    return result