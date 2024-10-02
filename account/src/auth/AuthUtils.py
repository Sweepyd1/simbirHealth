from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
import uuid

from ..schemas.auth import IsAuthenticated


class AuthUtils:
    
    def __init__(self,
                 ALGORITHM,
                 ACCESS_TOKEN_EXP,
                 REFRESH_TOKEN_EXP,
                 SECRET_KEY,
                 db
                 ):
        

        self.ALGORITHM = ALGORITHM
        self.ACCESS_TOKEN_EXP = ACCESS_TOKEN_EXP
        self.REFRESH_TOKEN_EXP = REFRESH_TOKEN_EXP
        self.SECRET_KEY = SECRET_KEY
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


        
    async def isAuthenticated(self, access_token: str, refresh_token: str) -> IsAuthenticated:

        if not access_token or not refresh_token:
            raise HTTPException(status_code=401, detail="Токены отсутствуют")

        payload_refresh_token = jwt.decode(refresh_token, self.SECRET_KEY, self.ALGORITHM)
        payload_access_token = jwt.decode(access_token, self.SECRET_KEY, self.ALGORITHM)

        if payload_refresh_token["id"] != payload_access_token["id"]:
            raise HTTPException(status_code=401, detail="Ошибка токенов")

        exp_refresh_token = payload_refresh_token.get("exp")
        exp_access_token = payload_access_token.get("exp")

        if exp_access_token is None or exp_refresh_token is None:
            raise HTTPException(status_code=401)

        current_timestamp = int(datetime.now().timestamp())

        if exp_refresh_token < current_timestamp:
            raise HTTPException(status_code=401)

        user = await self.db.get_user_by_id(payload_access_token["id"])

        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if user.to_dict()["refresh_token"] == refresh_token:
            new_access_token = self.create_access_token(payload_refresh_token)
            new_refresh_token = self.create_refresh_token(payload_refresh_token)
            await self.db.update_refresh_token(payload_access_token["id"], new_refresh_token)

            return IsAuthenticated(True, user.to_dict(), new_access_token, new_refresh_token)

        raise HTTPException(status_code=401, detail="Ошибка аутентификации")

            

            
            
                



        



        
    
    def verify_password(self,plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    
    def get_password_hash(self,password):
        return self.pwd_context.hash(password)
    
    def create_user_id(self):
        return str(uuid.uuid4())
    
    
    def create_access_token(self,data:dict)->str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=self.ACCESS_TOKEN_EXP)
    

        to_encode.update({"exp":expire})
        access_token = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        
        return access_token
    
    
    

    def create_refresh_token(self,data:dict)->str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(days=30)
        to_encode.update({"exp":expire})
        refresh_token = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
    
        return refresh_token