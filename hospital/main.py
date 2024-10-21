from fastapi import FastAPI, Request
from fastapi.responses import Response
from contextlib import asynccontextmanager


from src.api.hospital_router import protected
from src.api.existing_router import check_data
from loader import db
from loader import db_start
from src.database.database import Base
@asynccontextmanager
async def lifespan(_):
    async with db_start.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    await db.create_hospital()
    print("созданы больнцы")
   
    
    
    yield  
    


app = FastAPI(title="hospital", lifespan=lifespan)

@app.post("/set_tokens")
async def set_tokens(request: Request, response: Response):
    data = await request.json()
    
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    

    if access_token and refresh_token:
      
        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)
      
        
        return {"message": "Tokens set successfully"}
    
    return {"error": "Tokens not provided"}, 400



app.include_router(protected)

app.include_router(check_data)


