from ....src.loader import protected


@protected.get("/Hospitals")
async def get_hospitals():
    pass


@protected.get("/Hospitals/{id}")
async def get_hospitals_by_id(id):
    pass


@protected.get("/Hospitals/{id}/Rooms")
async def get_rooms_in_hospital(id):
    pass


@protected.post("/Hospitals")
async def create_hospital(id):
    pass



@protected.put("/Hospitals/{id}")
async def change_hospital(id):
    pass


@protected.put("/Hospitals/{id}")
async def delete_hospital(id):
    pass



