from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.account_router import protected
from src.api.router_auth import unprotected
import uvicorn
from src.database.database import DatabaseManager
from src.database.Crud import Crud
from config import DATABASE_URL


@asynccontextmanager
async def lifespan(_):
    db = Crud(DatabaseManager(DATABASE_URL))
    print("подключени")
    yield


app = FastAPI(lifespan=lifespan) #lifespan=lifespan

app.include_router(protected)
app.include_router(unprotected)

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000, reload=True)