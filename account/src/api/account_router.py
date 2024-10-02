from fastapi import Request, HTTPException

from fastapi.responses import Response

from ..auth.ProtectedAPIRouter import protected

# from loader import auth_utils


@protected.get("/Accounts/Me")
async def get_me(request: Request):
    user = request.state.user
    
    return user
    
    

    




@protected.get("/Accounts")
async def get_all_accounts():
    pass




@protected.put("/Accounts/Update")
async def update_account():
    pass





@protected.post("/Accounts")
async def create_new_account():
    pass



@protected.put("/Accounts/{id}")
async def update_account_by_id(id):
    pass


@protected.delete("/Accounts/{id}")
async def delete_account_by_id(id):
    pass



@protected.get("/Doctors")
async def get_all_doctors():
    pass


@protected.get("/Doctors/{id}")
async def get_doctor_info_by_id(id):
    pass