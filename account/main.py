from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.account_router import protected
from src.api.auth_router import unprotected
from src.api.existing_router import check_data
from loader import db
from loader import auth_utils, db_start
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import Response
from src.database.database import Base
import time
import uvicorn
import asyncio

@asynccontextmanager
async def lifespan(_):

    async with db_start.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await db.create_doctors()
    print("созданы докторы и базовые пользоатели")
    
    yield


app = FastAPI(lifespan=lifespan, title="account")
app.include_router(protected)
app.include_router(unprotected)
app.include_router(check_data)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8082","http://localhost:8081"],  # Adjust as necessary
    allow_credentials=True,  # Allow cookies to be sent
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/set_tokens")
async def set_tokens(request: Request, response: Response):
   
    data = await request.json()
    print(data)
    
    
    access_token = data["data"]["token"]
   
    

    if access_token:
        print(access_token)
      
        response.set_cookie("access_token", access_token, httponly=True, expires=data["data"]["expires"])
        print("токен установелн")
        
      
        
        return {"message": "Tokens set successfully"}
    
    return {"error": "Tokens not provided"}

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)