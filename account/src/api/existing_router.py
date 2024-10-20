from fastapi import APIRouter, Request
from loader import db

check_data = APIRouter(prefix="/api", tags=["проверка данных с других сервисов"])




@check_data.post("/check_doctor")
async def check_doctor(request:Request):
    data = await request.json()
    

    doctor_id = data["doctor_id"]

  
    result = await db.get_doctor_info_by_id(doctor_id)
    print(result.to_dict())
        
    if result:
        
            
        return {"existing": True}

    return {"existing": False}

        


