from fastapi import FastAPI, Request
from fastapi.responses import Response
from contextlib import asynccontextmanager
from src.api.document_router import protected
from fastapi.middleware.cors import CORSMiddleware
from loader import db_start
from src.database.database import Base


@asynccontextmanager
async def lifespan(_):
    async with db_start.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
 
   
    
    
    yield  
    


app = FastAPI(title="документы", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Adjust as necessary
    allow_credentials=True,  # Allow cookies to be sent
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.post("/set_tokens")
# async def set_tokens(request: Request, response: Response):
   
#     data = await request.json()
#     print(data)
    
    
#     access_token = data["data"]["token"]
   
    

#     if access_token:
#         print(access_token)
      
#         response.set_cookie("access_token", access_token, httponly=True, expires=data["data"]["expires"])
#         print("токен установелн")
        
      
        
#         return {"message": "Tokens set successfully"}
    
#     return {"error": "Tokens not provided"}

app.include_router(protected)