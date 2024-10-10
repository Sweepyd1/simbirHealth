from typing import Callable
from fastapi import APIRouter, HTTPException, Request
from fastapi.routing import APIRoute
from fastapi.responses import Response
import aiohttp




class CustomAPIRoute(APIRoute):

    def get_route_handler(self) -> Callable:
        handler = super().get_route_handler()

        async def get_status_auth_current_user(request: Request):
            access_token = request.cookies.get("access_token")

            if access_token:
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.post("http://localhost:8080/", json={
                            "access_token": access_token,
                        }) as resp:
                            if resp.status == 200:
                                print("Tokens sent successfully")
                            else:
                                print(f"Failed to send tokens: {resp.status}")
                    except Exception as e:
                        print(f"Error while sending tokens: {str(e)}")

            
          


       