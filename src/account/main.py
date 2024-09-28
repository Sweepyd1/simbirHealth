from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.account_router import protected
from api.router_auth import unprotected
# import uvicorn
from database.database import DatabaseManager
from database.Crud import Crud

@asynccontextmanager
async def lifespan():
    db = Crud(DatabaseManager())
    yield


app = FastAPI() #lifespan=lifespan

app.include_router(protected)
app.include_router(unprotected)

# if __name__ == "__main__":
#     uvicorn.run(app,host="localhost",port=8000, reload=True)