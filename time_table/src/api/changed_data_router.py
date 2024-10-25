from fastapi import Request, APIRouter
from loader import db

change_data = APIRouter(prefix="/api", tags=["синхронизация данных"])


#check
@change_data.post("/delete_all_record/{hospital_id}")
async def delete_all_hospital_record_by_id(request:Request,hospital_id:int):
    data = await request.json()
    service_token = data["service_token"]
    if service_token not in list_available_tokens:
        raise HTTPException(status_code=403, detail="access denied")

    result = await db.delete_time_table_for_hospital(hospital_id)
    return result


#check
@change_data.post("/change_all_record/{hospital_id}")
async def change_all_hospital_record_by_id(request:Request,hospital_id:int):
    data = await request.json()
    service_token = data["service_token"]
    if service_token not in list_available_tokens:
        raise HTTPException(status_code=403, detail="access denied")

    old_rooms = data["old_rooms"]
    new_rooms = data["new_rooms"]
    return await db.change_hospital_data(hospital_id,old_rooms,new_rooms)
    # print("комнаты поменяны")


#check
@change_data.post("/delete_all_record_doctor/{doctor_id}")
async def delete_all_record_doctor(request:Request,doctor_id:int):
    data = await request.json()
    service_token = data["service_token"]
    if service_token not in list_available_tokens:
        raise HTTPException(status_code=403, detail="access denied")
        
    result = await db.delete_all_record_for_doctor(doctor_id)
    return result