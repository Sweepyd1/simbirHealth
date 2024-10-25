from fastapi import FastAPI, Request
from fastapi.responses import Response
from contextlib import asynccontextmanager
from sqlalchemy import text

from src.api.hospital_router import protected
from src.api.existing_router import check_data
from loader import db
from loader import db_start
from src.database.database import Base
import httpx

@asynccontextmanager
async def lifespan(_):
    async with db_start.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # await conn.execute(text("ALTER SEQUENCE hospitals_id_seq RESTART WITH 1;"))    
    await db.create_hospital()
    print("созданы больнцы")

    yield
    

app = FastAPI(title="hospital", lifespan=lifespan)

app.include_router(protected)

app.include_router(check_data)


