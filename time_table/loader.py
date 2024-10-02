# функцию или целый класс  пеерписать под рэбит

from fastapi import APIRouter, Depends, HTTPException
import httpx
class ProtectedRouter(APIRouter):
    async def verify_token(self, token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get("http://auth-service/verify-token", headers={"Authorization": f"Bearer {token}"})
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")
            return response.json()



protected = ProtectedRouter(prefix="/api")
