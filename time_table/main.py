from fastapi import FastAPI, Request
from fastapi.responses import Response
from contextlib import asynccontextmanager
from src.api.time_table_router import protected
from src.api.changed_data_router import change_data
from fastapi.middleware.cors import CORSMiddleware

from loader import db_start
from src.database.database import Base
from sqlalchemy import text

@asynccontextmanager
async def lifespan(_):
    async with db_start.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # await conn.execute(text("ALTER SEQUENCE time_table_id_seq RESTART WITH 1;"))
    # await db.create_hospital()
    # print("созданы больнцы")
   
    yield
    
    


app = FastAPI(title="расписание", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8082","http://localhost:8081","http://localhost:8080"],  # Adjust as necessary
    allow_credentials=True,  # Allow cookies to be sent
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.post("/set_tokens")
# async def set_tokens(request: Request, response: Response):
#     print(1)
   
#     data = await request.json()
#     print(data)
    
    
#     access_token = data["token"]
   
    

#     if access_token:
#         print(access_token)
      
#         response.set_cookie(
#                 key="access_token",
#                 value=token["token"],
#                 httponly=True,
#                 expires=token["expires"],
#                 path="/",  # Убедитесь, что путь установлен корректно
#                 samesite='None',  # Если используется HTTPS, добавьте secure=True
#                   # Если ваш сервер работает по HTTPS
#             )
#         print("токен установелн")
        
      
        
#         return {"message": "Tokens set successfully"}
    
#     return {"error": "Tokens not provided"}

app.include_router(protected)
app.include_router(change_data)