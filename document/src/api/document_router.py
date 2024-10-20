
from ..schemas.schemas import HistorySchemas
from fastapi import APIRouter, Depends,HTTPException
from ..utils.utils import get_current_user
from loader import db
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
   
        
    

@protected.post("/History")
async def create_history(data:HistorySchemas, user = Depends(get_current_user)):
     if "doctor" in user["role"] or "manager" in user["role"] or "admin" in user["role"]:
        data.date = data.date.replace(tzinfo=None)

        result = await db.create_history(data)
        return result

        




@protected.put("/History/{id}")
async def put_history(id):
    pass





