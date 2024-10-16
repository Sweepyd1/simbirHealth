from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.account_router import protected
from src.api.auth_router import unprotected
import uvicorn

from loader import db
from loader import auth_utils

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(_):
  
    print("подключени")
    await db.create_doctors()
    print("созданы докторы и базовые пользоатели")
    
    
    yield


app = FastAPI(lifespan=lifespan, title="account")
app.include_router(protected)
app.include_router(unprotected)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8082"],  # Adjust as necessary
    allow_credentials=True,  # Allow cookies to be sent
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)