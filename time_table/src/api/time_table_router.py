from datetime import datetime, timezone

from ..schemas.schemas import TimetableEntry
from fastapi import HTTPException, APIRouter, Depends
from ..utils.utils import get_current_user
from loader import db
protected = APIRouter(prefix="/api", tags=["расписание"])




@protected.post("/api/Timetable")
async def create_new_time_table(entry: TimetableEntry, user=Depends(get_current_user)):
    print("Текущий пользователь:", user)
    
    if user["role"] in ["admin", "manager"]:
    
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

     


@protected.put("/Timetable/{id}")
async def update_time_table(id, entry: TimetableEntry, user=Depends(get_current_user)):
    if user["role"] in ["admin", "manager"]:
        id = int(id)
        result  = await db.get_timetable_info_by_id(id)
       
        result = result.to_dict()

#переписать вот этот блок кода с проверкой
        # if result["enrolled_user_id"] is None:
        from_dt = entry.from_.replace(tzinfo=None)  
        to_dt = entry.to.replace(tzinfo=None)  

        updated_entry = await db.update_time_table(
            id = id,
            hospitalId=entry.hospitalId,
            doctorId=entry.doctorId,
            from_=from_dt,
            to=to_dt,
            room=entry.room
            

            )  
    
    return {
        "message": "Timetable entry created successfully.",
        "entry": updated_entry
    }
    
    return "нельзя изменить запись, пользователь уже записан"

    raise HTTPException(status_code=403, detail="Access denied.")
  





@protected.delete("/Timetable/{id}")
async def delete_time_table(id, user=Depends(get_current_user)):
    if user["role"] in ["admin", "manager"]:
        id = int(id)
        result = await db.delete_time_table(id)
        return result



@protected.delete("/Timetable/Doctor/{id}")
async def delete_time_table_for_doctor(id, user=Depends(get_current_user)):
    if user["role"] in ["admin", "manager"]:
        id = int(id)
        result = await db.delete_time_table_for_doctor(id)
        return result


@protected.delete("/Timetable/Hospital/{id}")
async def delete_time_table_for_hospital(id, user=Depends(get_current_user)):
    if user["role"] in ["admin", "manager"]:
        id = int(id)
        result = await db.delete_time_table_for_hospital(id)
        return result



@protected.get("/Timetable/Hospital/{id}")
async def get_time_table_for_hospital(id:int, from_:datetime, to:datetime, user=Depends(get_current_user)):
     if user is not None:
        id = int(id)
        result = await db.get_timetable_for_hospital(id, from_, to)
        return result
        

    


@protected.get("/Timetable/Doctor/{id}")
async def get_time_table_for_doctor(id:int, from_:datetime, to:datetime, user=Depends(get_current_user)):
    if user is not None:
        id = int(id)
        result = await db.get_timetable_for_hospital(id, from_, to)
        return result


@protected.get("/Timetable/Hospital/{id}/Room/{room}")
async def get_time_table_a_room_in_hospital(id, room, from_:datetime, to:datetime, user=Depends(get_current_user)):
    if user is not None:
        id = int(id)
        result = await db.get_timetable_for_room_in_hospital(id,room, from_, to)
        return result



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












