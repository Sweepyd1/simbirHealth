import aiohttp



async def check_hospital(hospital_id):
    async with aiohttp.ClientSession() as session:
        try:
            
            async with session.post("http://localhost:8081/api/check_hospital", json={"hospital_id": hospital_id}) as resp:
                if resp.status == 200:
                   
                    return await resp.json()
                else:
                    print(f"Failed to send tokens: {resp.status}, Response: {await resp.text()}")
        except Exception as e:
            print(f"Error while sending tokens: {str(e)}")





async def check_doctor(doctor_id):
    async with aiohttp.ClientSession() as session:
        try:
            
            async with session.post("http://localhost:8080/api/check_doctor", json={"doctor_id": doctor_id}) as resp:
                if resp.status == 200:
                   
                    return await resp.json()
                else:
                    print(f"Failed to send tokens: {resp.status}, Response: {await resp.text()}")
        except Exception as e:
            print(f"Error while sending tokens: {str(e)}")


async def check_room_and_hospital(room_name, hospital_id):
    async with aiohttp.ClientSession() as session:
        try:

            async with session.post("http://localhost:8081/api/check_room_and_hospital", json={"hospital_id": hospital_id, "room_name":room_name}) as resp:
                if resp.status == 200:
                   
                    return await resp.json()
                else:
                    print(f"Failed to send tokens: {resp.status}, Response: {await resp.text()}")
        except Exception as e:
            print(f"Error while sending tokens: {str(e)}")