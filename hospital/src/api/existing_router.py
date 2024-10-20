from fastapi import APIRouter, Request, HTTPException
from loader import db

check_data = APIRouter(prefix="/api", tags=["проверка данных с других сервисов"])


@check_data.post("/check_hospital")
async def check_hospital(request:Request):
    data = await request.json()

    hospital_id = data.get("hospital_id")

    if hospital_id:
        result = await db.get_hospital_by_id(hospital_id)

        if result:
            return {"existing": True}

        return {"existing": False}
    return {"existing": False}



# @check_data.post("/check_doctor")
# async def check_doctor(request:Request):
#     data = await request.json()

#     doctor_id = data.get("doctor_id")

#     if doctor_id:
#         result = await db.get
        


@check_data.post("/check_room_and_hospital")
async def check_room(request: Request):
    try:
        data = await request.json()
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")

    room_name = data.get("room_name")
    hospital_id = data.get("hospital_id")

    if hospital_id is not None and room_name:
        # Получаем список комнат в больнице по ID
        result = await db.get_rooms_in_hospital_by_id(int(hospital_id))

        # Проверяем, есть ли комната с указанным именем
        for room in result:
            if room.name == room_name:  # Предполагается, что room - это объект с атрибутом name
                return {"existing": True}  # Возвращаем словарь с информацией о существовании

        return {"existing": False}  # Если ни одна комната не совпала

    return {"error": "Invalid input. Please provide both hospital_id and room_name."}