from fastapi import APIRouter, Request
from loader import db
from config import list_available_tokens
from fastapi import HTTPException

check_data = APIRouter(prefix="/api", tags=["проверка данных с других сервисов"])



##check token
@check_data.post("/check_doctor")
async def check_doctor(request:Request):
    data = await request.json()
    doctor_id = data["doctor_id"]
    service_token = data["service_token"]

    if service_token in list_available_tokens:
        print(service_token)
        result = await db.get_doctor_info_by_id(doctor_id)
        print(result.to_dict())
            
        if result:
            
                
            return {"existing": True}

        return {"existing": False}
    raise HTTPException(status_code=403,detail="access denied")

        


