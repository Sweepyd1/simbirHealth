from loader import protected

@protected.post("/Timetable")
async def create_new_time_table():
    pass

@protected.put("/Timetable/{id}")
async def update_time_table(id):
    pass



@protected.delete("/Timetable/{id}")
async def delete_time_table(id):
    pass


@protected.delete("/Timetable/Doctor/{id}")
async def delete_time_table_a_doctor(id):
    pass


@protected.delete("/Timetable/Hospital/{id}")
async def delete_time_table_a_hospital(id):
    pass



@protected.get("/Timetable/Hospital/{id}")
async def get_time_table_a_hospital(id):
    pass


@protected.get("/Timetable/Doctor/{id}")
async def get_time_table_a_doctor(id):
    pass


@protected.get("/Timetable/Hospital/{id}/Room/{room}")
async def get_time_table_a_room_in_hospital(id, room):
    pass


# переписать
@protected.get("/Timetable/{id}/Appointments")
async def get_free_talon(id):
    pass


@protected.post("/Timetable/{id}/Appointments")
async def post_na_priem(id):
    pass


@protected.delete("/Appointments/{id}")
async def otmena(id):
    pass












