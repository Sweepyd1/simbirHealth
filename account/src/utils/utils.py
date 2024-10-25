
import aiohttp
from config import TIME_TABLE_SERVER_URL, DOCUMENT_SERVER_URL, ACCOUNT_SERVICE_TOKEN

async def delete_all_record_with_doctor(doctor_id):
    async with aiohttp.ClientSession() as session:
        responses = []  # List to collect responses from each server
        for server in [DOCUMENT_SERVER_URL, TIME_TABLE_SERVER_URL]:
            try:
                async with session.post(f"{server}/api/delete_all_record_doctor/{doctor_id}", json={"service_token":ACCOUNT_SERVICE_TOKEN}) as resp:
                    response = await resp.json()
                    responses.append(response)  # Collect response from each server
            except Exception as e:
                # Handle exceptions (you can log them or return a specific error message)
                print(f"Error occurred while contacting {server}: {str(e)}")
                responses.append({"error": str(e)})  # Collect error information

        return {"is_changed": responses}  # Return all collected responses