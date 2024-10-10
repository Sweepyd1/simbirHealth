from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.account_router import protected
from src.api.auth_router import unprotected
import uvicorn

from loader import db
from loader import auth_utils
import aio_pika
import logging

import asyncio



@asynccontextmanager
async def lifespan(_):
  
    print("подключени")
    await db.create_doctors()
    print("созданы докторы и базовые пользоатели")
    
    
    yield


app = FastAPI(lifespan=lifespan, title="account")
app.include_router(protected)
app.include_router(unprotected)

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)