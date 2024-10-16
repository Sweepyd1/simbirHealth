from fastapi import Request, HTTPException

from fastapi.responses import Response



from ..schemas.account import UpdateAccount


from loader import db
from ..auth.ProtectedAPIRouter import protected

            
@protected.get("/Accounts/Me")
async def get_me(request: Request):
    user = request.state.user

    if user:
      
        return user

   
    

    
    

    




@protected.get("/Accounts")
async def get_all_accounts(request:Request):
    pass
    
   
    





@protected.put("/Accounts/Update")
async def update_account(account:UpdateAccount, request:Request):
    try:
        user = request.state.user
       
        update_data = account.dict(exclude_none=True) 
       
        await db.update_account_info(user["id"], **update_data)
        
        
    
        return "данные обновлены"
    except Exception as e:
        return e
    





@protected.post("/Accounts")
async def create_new_account(request:Request):
    user = request.state.user
    print(user)

    if user["role"] != "admin":
        return "у вас недостаточно прав"



@protected.put("/Accounts/{id}")
async def update_account_by_id(id):
    pass


@protected.delete("/Accounts/{id}")
async def delete_account_by_id(id):
    pass



@protected.get("/Doctors")
async def get_all_doctors(request:Request):
    user = request.state.user
    results = await db.get_all_doctors_from_db()
    return results

    

    


@protected.get("/Doctors/{id}")
async def get_doctor_info_by_id(id):
    pass