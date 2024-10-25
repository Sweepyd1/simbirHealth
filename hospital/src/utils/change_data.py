from fastapi import HTTPException
from fastapi import Request
import aiohttp
from datetime import datetime
from fastapi.responses import Response
from ..schemas.hospitals import HospitalSchema
from config import ACCOUNT_SERVER_URL, TIME_TABLE_SERVER_URL, DOCUMENT_SERVER_URL, HOSPITAL_SERVICE_TOKEN


##request to timetable and document
async def delete_all_record_with_hospital(hospital_id: int):
    response = None  # Initialize response variable
    for server in [DOCUMENT_SERVER_URL, TIME_TABLE_SERVER_URL]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{server}/api/delete_all_record/{hospital_id}", json={"service_token":HOSPITAL_SERVICE_TOKEN}) as resp:
                    response = await resp.json()
            except Exception as e:
                return {"error": str(e)}  # Return error details
            # No need for a finally block here; we can return directly after processing

    return {"is_changed": response} if response else {"error": "No response from servers."}



##request to timetable and document
async def change_all_record_with_hospital(hospital_id:int,new_rooms:list, old_rooms:list):
    async with aiohttp.ClientSession() as session:
        for server in [DOCUMENT_SERVER_URL, TIME_TABLE_SERVER_URL]:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(f"{server}/api/change_all_record/{hospital_id}", json={"new_rooms":new_rooms, "old_rooms":old_rooms,"service_token":HOSPITAL_SERVICE_TOKEN}) as resp:
                        print("данные отправид")
                        response = await resp.json()
                except Exception as e:
                    return {"error": str(e)}  # Return error details
            # No need for a finally block here; we can return directly after processing

    return {"is_changed": response} if response else {"error": "No response from servers."}
