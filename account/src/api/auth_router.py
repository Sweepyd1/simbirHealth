from datetime import datetime, timedelta
from fastapi import APIRouter,Request,Cookie, HTTPException, Query
from fastapi.responses import Response
from .account_router import protected  
from ..schemas.auth import RegistrationUser, LoginUser, TokenData
from loader import auth_utils
from loader import db
from config import list_available_tokens
import aiohttp

from config import HOSPITAL_SERVER_URL, TIME_TABLE_SERVER_URL
unprotected = APIRouter(prefix="/api")

@unprotected.post("/Authentication/SignUp")
async def sign_up(user_data: RegistrationUser, response: Response):
    if not user_data:
        raise HTTPException(status_code=400, detail="User data is required.")

    existing_user = await db.get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists.")

    try:
        # user_id = auth_utils.create_user_id()
        hashed_password = auth_utils.get_password_hash(user_data.password)
        result = await db.create_user(user_data.username, user_data.firstName,user_data.lastName,hashed_password,["user"])

        access_token = auth_utils.create_access_token({"id": result.id, "role": ["user"]})
        refresh_token = auth_utils.create_refresh_token({"id": result.id, "role": ["user"]})

        access_exp = auth_utils.decode_token(access_token)["exp"]
        refresh_exp = auth_utils.decode_token(refresh_token)["exp"]

        response.set_cookie("access_token", access_token, httponly=True, expires=access_exp)
        response.set_cookie("refresh_token", refresh_token, httponly=True, expires=refresh_exp)

        await db.update_refresh_token(result.id, refresh_token)

       

        return {"status_code": 200, "detail": "User created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@unprotected.post("/Authentication/SignIn")
async def sign_in(user_data: LoginUser, response: Response):
    user = await db.get_user_by_username(user_data.username)
    if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password.")
      
    is_correct_password = auth_utils.verify_password(user_data.password, user.password)
    
    if is_correct_password:
        
       

        try:
            access_token = auth_utils.create_access_token({"id": user.id, "role": user.role})
            refresh_token = auth_utils.create_refresh_token({"id": user.id, "role": user.role})

            access_exp = auth_utils.decode_token(access_token)["exp"]
            refresh_exp = auth_utils.decode_token(refresh_token)["exp"]

            await db.update_refresh_token(int(user.id), refresh_token)

            response.set_cookie("access_token", access_token, httponly=True, expires=access_exp)
            response.set_cookie("refresh_token", refresh_token, httponly=True, expires=refresh_exp)

            async with aiohttp.ClientSession() as session:
                for url in [f"{HOSPITAL_SERVER_URL}/set_tokens", f"{TIME_TABLE_SERVER_URL}/set_tokens"]:
                    try:
                        async with session.post(url, json={
                            "access_token": access_token,
                            "refresh_token": refresh_token
                        }) as resp:
                            if resp.status == 200:
                                print(f"Tokens sent successfully to {url}")
                            else:
                                print(f"Failed to send tokens to {url}: {resp.status}")
                    except Exception as e:
                        print(f"Error while sending tokens to {url}: {str(e)}")

            return {"status_code": 200, "detail": "Successfully signed in and tokens updated."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=401, detail="wrong username or password")


@unprotected.put("/Authentication/SignOut")
async def sign_out(response: Response):
    response.delete_cookie(key="access_token", httponly=True)
    response.delete_cookie(key="refresh_token", httponly=True)
    return {"status_code": 200, "detail": "Tokens deleted and you have signed out."}


#check tokens
@unprotected.get("/Authentication/Validate")
async def validate(accessToken: str = Query(...)):
    try:
        user = auth_utils.decode_token(accessToken)

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token.")

        expiration_time = datetime.fromtimestamp(user.get("exp"))
        current_time = datetime.utcnow()
        
        is_active = current_time < expiration_time

        token_data = TokenData(
            token=accessToken,
            isActive=is_active,
            user=user  
        )
        
        return {"status_code": 200, "token_data": token_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


##check token
@unprotected.post("/Authentication/Refresh")
async def refresh(request: Request, response: Response):
    data = await request.json()
 
    if "refresh_token" not in data:
        raise HTTPException(status_code=400, detail="Refresh token is required.")

    refresh_token = data["refresh_token"]

    payload = auth_utils.decode_token(refresh_token)
       
    access_token = auth_utils.create_access_token(payload)
    return access_token




    
    






