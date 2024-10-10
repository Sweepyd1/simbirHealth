from typing import Callable
from fastapi import APIRouter, HTTPException, Request
from fastapi.routing import APIRoute
from fastapi.responses import Response

from loader import auth_utils
from loader import db 

from jose import jwt, JWTError
from datetime import datetime, timedelta

class CustomAPIRoute(APIRoute):

    def get_route_handler(self) -> Callable:
        handler = super().get_route_handler()

        async def get_status_auth_current_user(request: Request):
            access_token = request.cookies.get("access_token")
            refresh_token = request.cookies.get("refresh_token")
            
            isAuthenticated_user = await auth_utils.isAuthenticated(access_token=access_token, refresh_token=refresh_token)
            

            if isAuthenticated_user.is_authenticated:
                request.state.user = isAuthenticated_user.user
                
                        
            
                response = await handler(request)

                response.set_cookie("access_token", isAuthenticated_user.access_token, httponly=True)
                response.set_cookie("refresh_token", isAuthenticated_user.refresh_token, httponly=True)

                
            
                return response
            print(isAuthenticated_user.is_authenticated)
            return "авторизуйтесь заново"
            
            
        return get_status_auth_current_user

protected = APIRouter(prefix="/api", route_class=CustomAPIRoute)
			
          
			
			
    





