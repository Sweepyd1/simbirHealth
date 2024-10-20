from fastapi import Request, HTTPException
from fastapi.responses import Response
from ..schemas.account import UpdateAccount, UserResponse,DoctorResponse
from loader import db
from ..auth.ProtectedAPIRouter import protected
from typing import Any,List


@protected.get("/Accounts/Me")
async def get_me(request: Request):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    print(user)
    return user


@protected.get("/Accounts")
async def get_all_accounts(request: Request, from_: int, count: int) -> list[UserResponse]:
    user = request.state.user
    if not user:
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        result = await db.get_all_accounts(from_, count)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

############
@protected.put("/Accounts/Update")
async def update_account(account: UpdateAccount, request: Request) -> str:
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:
        update_data = account.dict(exclude_none=True)
        await db.update_account_info(user["id"], **update_data)
        return "Данные обновлены"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

##############
@protected.post("/Accounts")
async def create_new_account(
    request: Request,
    lastName: str,
    firstName: str,
    username: str,
    password: str,
    roles: list[str]
) -> Any:

    user = request.state.user
    print(user["role"])
    if "admin" not in user["role"]:
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        result = await db.create_account_by_admin(lastName, firstName, username, password, roles)
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected.put("/Accounts/{id}")
async def update_account_by_id(
    id: int,
    request: Request,
    lastName: str,
    firstName: str,
    username: str,
    password: str,
    roles: list[str]
) -> Any:

    user = request.state.user
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        result = await db.update_account_by_admin(id, lastName, firstName, username, password, roles)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected.delete("/Accounts/{id}")
async def delete_account_by_id(id: int, request: Request) -> Any:
    user = request.state.user
    if "admin" not in user["role"]:
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        result = await db.delete_account_by_admin(id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected.get("/Doctors")
async def get_all_doctors(request: Request, from_: int, count: int) -> list[DoctorResponse]:
    try:
        results = await db.get_all_doctors_from_db(from_, count)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected.get("/Doctors/{id}")
async def get_doctor_info_by_id(id: int, request: Request) -> DoctorResponse:
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    try:
        result = await db.get_doctor_info_by_id(id)
        if not result:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
