import aiohttp
from config import HOSPITAL_SERVER_URL, ACCOUNT_SERVER_URL, TIME_TABLE_SERVICE_TOKEN


async def check_hospital(hospital_id):
    async with aiohttp.ClientSession() as session:
        try:
            
            async with session.post(f"{HOSPITAL_SERVER_URL}/api/check_hospital", json={"hospital_id": hospital_id, "service_token":TIME_TABLE_SERVICE_TOKEN}) as resp:
                if resp.status == 200:
                   
                    return await resp.json()
                else:
                    print(f"Failed to send tokens: {resp.status}, Response: {await resp.text()}")
        except Exception as e:
            print(f"Error while sending tokens: {str(e)}")





async def check_doctor(doctor_id):
    async with aiohttp.ClientSession() as session:
        try:
            
            async with session.post(f"{ACCOUNT_SERVER_URL}/api/check_doctor", json={"doctor_id": doctor_id, "service_token":TIME_TABLE_SERVICE_TOKEN}) as resp:
                if resp.status == 200:
                   
                    return await resp.json()
                else:
                    print(f"Failed to send tokens: {resp.status}, Response: {await resp.text()}")
        except Exception as e:
            print(f"Error while sending tokens: {str(e)}")


async def check_room_and_hospital(room_name, hospital_id):
    async with aiohttp.ClientSession() as session:
        try:

            async with session.post(f"{HOSPITAL_SERVER_URL}/api/check_room_and_hospital", json={"hospital_id": hospital_id, "room_name":room_name,"service_token":TIME_TABLE_SERVICE_TOKEN}) as resp:
                if resp.status == 200:
                   
                    return await resp.json()
                else:
                    print(f"Failed to send tokens: {resp.status}, Response: {await resp.text()}")
        except Exception as e:
            print(f"Error while sending tokens: {str(e)}")