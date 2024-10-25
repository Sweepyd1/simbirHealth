from ..schemas.schemas import HistorySchemas
from fastapi import APIRouter, Depends,HTTPException
from ..utils.utils import get_current_user
from loader import db, es
from ..utils.check_unique import check_room_and_hospital, check_doctor
from typing import List
protected = APIRouter(prefix="/api", tags=["сервис документов"])

# protected_role = ["admin", "manager", "doctor"]

@protected.get("/History/account/{id}")
async def get_account_history(id_pacient, user = Depends(get_current_user)):
     if "doctor" in user["role"] or user["id"] == id_pacient:
        result = await db.get_history_for_pacient(int(id_pacient))

        return result


    


@protected.get("/History/{id}")
async def get_full_history_by_id(history_id:int,user = Depends(get_current_user)):
    result = await db.get_history_by_id(int(history_id))
    result = result[0].to_dict()

  

    if result is None:
        raise HTTPException(status_code=404, detail="History not found")

    # Проверка прав доступа
    if "doctor" in user["role"] or int(user["id"]) == result["pacient_id"]:
        return result
    
 
    raise HTTPException(status_code=403, detail="Access denied")
   
        
    
##добавить проверку на существование больницы и комнаты
@protected.post("/History")
async def create_history(data:HistorySchemas, user = Depends(get_current_user)):
    
    
    is_exesting_hospital_and_room = await check_room_and_hospital(data.room,data.hospital_id)
    is_existing_doctor = await check_doctor(data.doctor_id)

    if is_exesting_hospital_and_room["existing"] and is_existing_doctor["existing"]:
        if "doctor" in user["role"] or "manager" in user["role"] or "admin" in user["role"]:
            data.date = data.date.replace(tzinfo=None)

            result = await db.create_history(data)
            return result
    raise HTTPException(status_code=404, detail="data not existing.")

        




@protected.put("/History/{id}")
async def put_history(history_id:int, data:HistorySchemas, user = Depends(get_current_user)):
    is_exesting_hospital_and_room = await check_room_and_hospital(data.room,data.hospital_id)
    is_existing_doctor = await check_doctor(data.doctor_id)

    if is_exesting_hospital_and_room["existing"] and is_existing_doctor["existing"]:
        if "doctor" in user["role"] or "manager" in user["role"] or "admin" in user["role"]:
            data.date = data.date.replace(tzinfo=None)

            result = await db.update_history(history_id,data)
            return result
    raise HTTPException(status_code=404, detail="data not existing.")

@protected.post("/search", response_model=List[dict])
async def search_data(query: str):
    try:
        response = await es.search(
            index="history",
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["data", "room"],  # Укажите поля для поиска
                        "type": "best_fields"  # Или используйте "most_fields" в зависимости от ваших нужд
                    }
                }
            }
        )

        results = [
            {
                "id": hit["_source"]["id"],
                "date": hit["_source"]["date"],
                "pacient_id": hit["_source"]["pacient_id"],
                "hospital_id": hit["_source"]["hospital_id"],
                "doctor_id": hit["_source"]["doctor_id"],
                "room": hit["_source"]["room"],
                "data": hit["_source"]["data"]
            }
            for hit in response["hits"]["hits"]
        ]

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



