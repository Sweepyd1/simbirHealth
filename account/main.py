from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.account_router import protected
from src.api.auth_router import unprotected
import uvicorn

from loader import db


@asynccontextmanager
async def lifespan(_):
  
    print("подключени")
    await db.create_doctors()
    yield


app = FastAPI(lifespan=lifespan) #lifespan=lifespan

app.include_router(protected)
app.include_router(unprotected)

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)