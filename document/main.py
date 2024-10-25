from fastapi import FastAPI, Request
from fastapi.responses import Response
from contextlib import asynccontextmanager
from src.api.document_router import protected
from src.api.changed_data_router import change_data
from fastapi.middleware.cors import CORSMiddleware
from loader import db_start, create_index_if_not_exists, index_history_records, DatabaseManager, DATABASE_URL
from src.database.database import Base
from sqlalchemy import text

database_manager = DatabaseManager(DATABASE_URL)

@asynccontextmanager
async def lifespan(_):
    async with db_start.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # await conn.execute(text("ALTER SEQUENCE history_id_seq RESTART WITH 1;"))

    await create_index_if_not_exists("history")
    await index_history_records(database_manager)
    yield  
    

app = FastAPI(title="документы", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Adjust as necessary
    allow_credentials=True,  # Allow cookies to be sent
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(protected)
app.include_router(change_data)