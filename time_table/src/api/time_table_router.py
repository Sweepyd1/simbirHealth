from datetime import datetime, timezone

from ..schemas.schemas import TimetableEntry
from fastapi import HTTPException, APIRouter, Depends
from ..utils.utils import get_current_user
from ..utils.check_unique import check_room_and_hospital, check_doctor, check_hospital
from loader import db

protected = APIRouter(prefix="/api", tags=["расписание"])



#check good
@protected.post("/api/Timetable")
async def create_new_time_table(entry: TimetableEntry, user=Depends(get_current_user)):
    # print("Текущий пользователь:", user)

    is_exesting = await check_room_and_hospital(entry.room, entry.hospitalId)

    if is_exesting["existing"]:
        if "admin" not in user["role"] or "manager" not in user["role"]:
        
            from_dt = entry.from_.replace(tzinfo=None)  
            to_dt = entry.to.replace(tzinfo=None)  

            created_entry = await db.create_time_table(
                hospitalId=entry.hospitalId,
                doctorId=entry.doctorId,
                from_=from_dt,
                to=to_dt,
                room=entry.room
                

            )  
            
            return {
                "message": "Timetable entry created successfully.",
                "entry": created_entry
            }
        
        raise HTTPException(status_code=403, detail="Access denied.")
    raise HTTPException(status_code=404, detail="Timetable not existing.")

     

#check goot
@protected.put("/Timetable/{id}")
async def update_time_table(id: int, entry: TimetableEntry, user=Depends(get_current_user)):
    # Проверка существования комнаты и больницы
    is_existing = await check_room_and_hospital(entry.room, entry.hospitalId)
    print(user)

    if not is_existing["existing"]:
        raise HTTPException(status_code=404, detail="Room or hospital does not exist.")

    # Проверка ролей пользователя
    if "admin" not in user["role"] and "manager" not in user["role"]:
        raise HTTPException(status_code=403, detail="Access denied for updating timetable by admin/manager.")

   
    timetable_entry = await db.get_timetable_info_by_id(id)

    if timetable_entry is None:
        raise HTTPException(status_code=404, detail="Timetable entry not found.")


    timetable_entry = timetable_entry.to_dict()

    # Обработка временных меток
    from_dt = entry.from_.replace(tzinfo=None)
    to_dt = entry.to.replace(tzinfo=None)

 
    updated_entry = await db.update_time_table(
        id=id,
        hospitalId=entry.hospitalId,
        doctorId=entry.doctorId,
        from_=from_dt,
        to=to_dt,
        room=entry.room
    )

    return {
        "message": "Timetable entry updated successfully.",
        "entry": updated_entry
    }
  





@protected.delete("/Timetable/{id}")
async def delete_time_table(id, user=Depends(get_current_user)):
    if "admin" not in user["role"] and "manager" not in user["role"]:
        id = int(id)
        result = await db.delete_time_table(id)
        return result



@protected.delete("/Timetable/Doctor/{id}")
async def delete_time_table_for_doctor(id, user=Depends(get_current_user)):
    if "admin" not in user["role"] and "manager" not in user["role"]:
        id = int(id)
        result = await db.delete_time_table_for_doctor(id)
        return result


@protected.delete("/Timetable/Hospital/{id}")
async def delete_time_table_for_hospital(id, user=Depends(get_current_user)):
    if "admin" not in user["role"] and "manager" not in user["role"]:
        id = int(id)
        result = await db.delete_time_table_for_hospital(id)
        return result


#check good
@protected.get("/Timetable/Hospital/{id}")
async def get_time_table_for_hospital(hospital_id:int, from_:datetime, to:datetime, user=Depends(get_current_user)):
    is_exesting = await check_hospital(hospital_id)
    if is_exesting["existing"]:
        if user is not None:
            hospital_id = int(hospital_id)
            result = await db.get_timetable_for_hospital(hospital_id, from_, to)
            return result
    return HTTPException(status_code=404, detail="Hospital not existing.")
        

    

#check
@protected.get("/Timetable/Doctor/{id}")
async def get_time_table_for_doctor(id:int, from_:datetime, to:datetime, user=Depends(get_current_user)):
    is_exesting = await check_doctor(id)
    print(is_exesting)
    if is_exesting["existing"]:
        if user is not None:
            print(user)
            id = int(id)
            result = await db.get_timetable_for_doctor(id, from_, to)
            return result
    raise HTTPException(status_code=404, detail="Doctor not existing.")

#check
@protected.get("/Timetable/Hospital/{id}/Room/{room}")
async def get_time_table_a_room_in_hospital(id, room, from_:datetime, to:datetime, user=Depends(get_current_user)):
    is_exesting = await check_room_and_hospital(room,id)
    if is_exesting["existing"]:
        if user is not None:
            id = int(id)
            result = await db.get_timetable_for_room_in_hospital(id,room, from_, to)
            return result
    raise HTTPException(status_code=404, detail="Timetable not existing.")



@protected.get("/Timetable/{id}/Appointments")
async def get_free_talon(id, user=Depends(get_current_user)):
     if user is not None:
        id = int(id)
        result = await db.get_timetable_butchered(id)
        return result
       


@protected.post("/Timetable/{id}/Appointments")
async def subscribe_to_appointments(id, from_:datetime, user=Depends(get_current_user)):
    if user is not None:
        id = int(id)
        result = await db.subscribe_to_appointments(id, int(user["id"]),from_)
        return result
    


@protected.delete("/Appointments/{id}")
async def delete_appointments(id, user=Depends(get_current_user)):
    if user is not None:
        id = int(id)
        result = await db.delete_to_appointments(id, int(user["id"]))
        return result












