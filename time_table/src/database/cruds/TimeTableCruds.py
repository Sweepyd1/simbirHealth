from ..database import DatabaseManager

from ..models import TimeTable, Butchured_time_table
from datetime import datetime
from ...schemas.schemas import TimetableEntry
from sqlalchemy.future import select
from sqlalchemy.orm import query
from sqlalchemy import delete, insert
from datetime import timedelta

def generate_time_intervals(start_time, end_time, interval_minutes=30):
    intervals = []
    current_time = start_time
    
    while current_time < end_time:
        next_time = current_time + timedelta(minutes=interval_minutes)
        intervals.append((current_time, next_time))
        current_time = next_time
        
    return intervals

class TimeTableCRUD:
    db_manager: DatabaseManager

   

    async def create_time_table(self, hospitalId: int, doctorId: int, from_, to, room: str):
        async with self.db_manager.get_session() as session:
            # Проверка на существование записи с теми же параметрами
            # query = select(TimeTable).where(
            #     TimeTable.hospitalId == hospitalId,
            #     TimeTable.doctorId == doctorId,
            #     TimeTable.room == room
            # )
            # result = await session.execute(query)
            # existing_entry = result.scalars().first()

            # if existing_entry:
            #     return "Запись с такими параметрами уже существует"

            # Проверка на пересечение временных интервалов
            overlap_query = select(TimeTable).where(
                TimeTable.hospitalId == hospitalId,
                TimeTable.doctorId == doctorId,
                TimeTable.from_ < to,  # Новый from_ должен быть меньше существующего to
                TimeTable.to > from_    # Новый to должен быть больше существующего from_
            )
            overlap_result = await session.execute(overlap_query)
            overlapping_entry = overlap_result.scalars().first()

            if overlapping_entry:
                return "Запись пересекается с существующим временным интервалом"

            # Создание новой записи в TimeTable
            new_entry = TimeTable(
                hospitalId=hospitalId,
                doctorId=doctorId,
                from_=from_,
                to=to,
                room=room
            )

            # Добавление новой записи в сессию
            session.add(new_entry)
            
            # Коммит для получения ID новой записи
            await session.commit()

            # Генерация временных интервалов
            intervals = generate_time_intervals(from_, to)

            # Создание записей в ButchuredTimeTable для каждого интервала
            for start, end in intervals:
                new_butchared_entry = Butchured_time_table(
                    id_time_table=new_entry.id,  # Указываем внешний ключ
                    from_=start,
                    to=end,
                    enrolled_user_id=None  # Или укажите конкретного пользователя, если нужно
                )
                session.add(new_butchared_entry)

            # Коммит для сохранения всех новых записей в ButchuredTimeTable
            await session.commit()

            return new_entry


    async def get_timetable_info_by_id(self,id:int):
        async with self.db_manager.get_session() as session:
            result = await session.execute(select(TimeTable).where(TimeTable.id == id))
            return result.scalars().first()



    async def update_time_table(self, id: int, hospitalId: int, doctorId: int, from_, to, room: str):
        async with self.db_manager.get_session() as session:
            # Удаляем все записи из Butchured_time_table для данного id_time_table
            await session.execute(
                delete(Butchured_time_table).where(Butchured_time_table.id_time_table == id)
            )

            # Получаем запись из TimeTable
            time_table_result = await session.execute(
                select(TimeTable).where(TimeTable.id == id)
            )
            time_table_entry = time_table_result.scalars().first()
            
            if time_table_entry:
                # Обновляем запись в TimeTable
                time_table_entry.hospitalId = hospitalId
                time_table_entry.doctorId = doctorId
                time_table_entry.from_ = from_
                time_table_entry.to = to
                time_table_entry.room = room
                
                # Генерация новых временных интервалов
                intervals = generate_time_intervals(from_, to)

                # Создаем новые записи в Butchured_time_table для каждого интервала
                for start, end in intervals:
                    new_butchured_entry = Butchured_time_table(
                        id_time_table=id,
                        from_=start,
                        to=end,
                        enrolled_user_id=None  # Или укажите конкретного пользователя, если нужно
                    )
                    session.add(new_butchured_entry)

                await session.commit()  # Коммитим изменения
                
                return {
                    "message": "Запись успешно обновлена.",
                    "updated_entry": time_table_entry.to_dict()  # Возвращаем обновленную запись
                }
            
            return "Запись не найдена."


    async def delete_time_table(self,id):
        async with self.db_manager.get_session() as session:
            result = await session.execute(delete(TimeTable).where(TimeTable.id==id))
            await session.commit()
        
            return result.rowcount

    async def delete_time_table_for_doctor(self,doctor_id):
         async with self.db_manager.get_session() as session:
            result = await session.execute(delete(TimeTable).where(TimeTable.doctorId==doctor_id))
            await session.commit()
        
            return result.rowcount



    async def delete_time_table_for_doctor(self,hospital_id):
         async with self.db_manager.get_session() as session:
            result = await session.execute(delete(TimeTable).where(TimeTable.hospitalId==hospital_id))
            await session.commit()
        
            return result.rowcount



    async def get_timetable_for_hospital(self, hospital_id, from_, to):
        async with self.db_manager.get_session() as session:
            # Execute the query to get all timetable entries for the specified hospital
            result = await session.execute(
                select(TimeTable).where(TimeTable.hospitalId == hospital_id)
            )
            
            # Fetch all results
            time_tables = result.scalars().all()

            # Check if any results were found
            if not time_tables:
                print("No timetable entries found for the specified hospital.")
                return []  # Return an empty list or handle as needed

            # Initialize a list to hold results from Butchured_time_table
            butchured_results = []

            # Iterate over each timetable entry
            for time_table in time_tables:
                id = time_table.to_dict()["id"]
                print(time_table.to_dict())  # Optional: Print each entry for debugging
                
                # Query Butchured_time_table for each timetable entry
                query = select(Butchured_time_table).where(
                    Butchured_time_table.id_time_table == id,
                    Butchured_time_table.to <= to,
                    Butchured_time_table.from_.between(from_, to)
                )
                request = await session.execute(query)

                # Append the results to the butchured_results list
                butchured_results.extend(request.scalars().all())

            return butchured_results  # Return all results from Butchured_time_table

    async def get_timetable_for_doctor(self, doctor_id, from_, to):
        async with self.db_manager.get_session() as session:
            # Execute the query to get all timetable entries for the specified doctor
            result = await session.execute(
                select(TimeTable).where(
                    TimeTable.doctorId == doctor_id,
                    TimeTable.from_.between(from_, to)  # Filter by the specified time range
                )
            )
            
            # Fetch all results
            time_tables = result.scalars().all()

            # Check if any results were found
            if not time_tables:
                print("No timetable entries found for the specified doctor.")
                return []  # Return an empty list or handle as needed

            # Initialize a list to hold results from Butchured_time_table
            butchured_results = []

            # Iterate over each timetable entry
            for time_table in time_tables:
                id = time_table.to_dict()["id"]
                print(time_table.to_dict())  # Optional: Print each entry for debugging
                
                # Query Butchured_time_table for each timetable entry
                query = select(Butchured_time_table).where(
                    Butchured_time_table.id_time_table == id,
                    Butchured_time_table.to <= to,
                    Butchured_time_table.from_.between(from_, to)
                )
                request = await session.execute(query)

                # Append the results to the butchured_results list
                butchured_results.extend(request.scalars().all())

            return butchured_results


######################################################################


    async def get_timetable_for_room_in_hospital(self, hospital_id, room, from_, to):
        async with self.db_manager.get_session() as session:
            # Execute the query to get all timetable entries for the specified room in the hospital
            result = await session.execute(
                select(TimeTable).where(
                    TimeTable.hospitalId == hospital_id,
                    TimeTable.room == room,
                    TimeTable.from_.between(from_, to)  
                )
            )
            
            # Fetch all results
            time_tables = result.scalars().all()

            # Check if any results were found
            if not time_tables:
                print("No timetable entries found for the specified room in the hospital.")
                return []  # Return an empty list or handle as needed

            # Initialize a list to hold results from Butchured_time_table
            butchured_results = []

            # Iterate over each timetable entry
            for time_table in time_tables:
                id = time_table.to_dict()["id"]
                print(time_table.to_dict())  # Optional: Print each entry for debugging
                
                # Query Butchured_time_table for each timetable entry
                query = select(Butchured_time_table).where(
                    Butchured_time_table.id_time_table == id,
                    Butchured_time_table.to <= to,
                    Butchured_time_table.from_.between(from_, to)
                )
                request = await session.execute(query)

                # Append the results to the butchured_results list
                butchured_results.extend(request.scalars().all())

            return butchured_results  # Return all results from Butchured_time_table







######################################################################

######################################################################






    async def get_timetable_butchered(self, id):
        async with self.db_manager.get_session() as session:
            # Получаем запись по ID
            query = select(TimeTable).where(TimeTable.id == id)
            result = await session.execute(query)
            record = result.scalars().first()
            
            if record:
                start_time = record.from_
                end_time = record.to
                
                # Генерируем интервалы
                time_intervals = generate_time_intervals(start_time, end_time)

                return time_intervals  # Возвращаем интервалы в виде списка кортежей (start, end)
            else:
                return []


    async def subscribe_to_appointments(self, id, user_id, from_):
        async with self.db_manager.get_session() as session:
            # Query to check if the appointment slot is available
            query = select(Butchured_time_table).where(
                Butchured_time_table.id_time_table == id,
                Butchured_time_table.from_ == from_
            )
            result = await session.execute(query)

            # Fetch the first result
            appointment = result.scalars().first()

            # Check if the appointment exists
            if not appointment:
                return "Appointment not found."

            # Check if the spot is already taken
            enrolled_user_id = appointment.to_dict().get("enrolled_user_id")
            if enrolled_user_id is not None:
                return "Sorry, this spot is already taken."

            # If the spot is free, update the appointment with the user's ID
            appointment.enrolled_user_id = user_id  # Assuming this field exists in your model

            # Commit the changes to save the enrollment
            session.add(appointment)  # Add the updated appointment to the session
            await session.commit()  # Commit changes to the database

            return "Successfully subscribed to the appointment."
            
            


    async def delete_to_appointments(self, id, user_id):
        async with self.db_manager.get_session() as session:
             query = select(Butchured_time_table).where(
                Butchured_time_table.id == id,
                Butchured_time_table.enrolled_user_id== user_id
            )
             result = await session.execute(query)

            # Fetch the first result
             appointment = result.scalars().first()

             if not appointment:
                return "Appointment not found."
            

             appointment.enrolled_user_id = None

             session.add(appointment)  # Add the updated appointment to the session
             await session.commit()  # Commit changes to the database

             return "Successfully delete to the appointment."



      


            
                
    
         
  

    
             
	


    
	

