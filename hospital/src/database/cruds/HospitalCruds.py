from sqlalchemy import func, select, between, delete
from ..database import DatabaseManager
from ...schemas.hospitals import HospitalSchema
from fastapi import HTTPException
from ..models import Hospital, Room
from fastapi import HTTPException
class HospitalCRUD:
	db_manager: DatabaseManager


	# async def create_rooms(self,):
	# 	async with self.db_manager.get_session() as session:
	# 		pass
	


	async def create_hospital(self):
		async with self.db_manager.get_session() as session:
			result = await session.execute(select(func.count()).select_from(Hospital))
			count = result.scalar() 

			if count == 0:  # Если таблица пуста
				hospitals_list = []

				# Генерация 50 больниц
				for i in range(1, 500):  # Генерируем 100 больниц
					hospital = Hospital(
						name=f"Госпиталь №{i}",
						address=f"Улица Примерная, {i}",
						phone=f"+7 (123) 456-78-{90 + i % 10}",  # Примерный телефон
						rating=round(4.0 + (i % 5) * 0.1, 1),  # Генерация рейтинга от 4.0 до 4.9
						email=f"hospital{i}@example.com",
						city="Город " + f"{i}"  # Примерный город
					)
					
					# Создание комнат для каждой больницы
					rooms_list = []
					for j in range(1, 21):  # Генерация 20 комнат для каждой больницы
						room = Room(
							name=f"Комната {j} в Госпитале №{i}",
							hospital=hospital  # Устанавливаем связь с больницей
						)
						rooms_list.append(room)

					hospital.rooms = rooms_list  # Добавляем комнаты к больнице
					hospitals_list.append(hospital)

				# Добавляем больницы в сессию
				session.add_all(hospitals_list)
				await session.commit()

	async def get_all_hospital(self, from_: int, count: int):
		async with self.db_manager.get_session() as session:
			# Используем BETWEEN для получения записей с id в диапазоне
			result = await session.execute(
				select(Hospital).where(Hospital.id >= from_).limit(count)
			)
			return result.scalars().all() 
		

	async def get_hospital_by_id(self, id):
		async with self.db_manager.get_session() as session:
			
			result = await session.execute(
				select(Hospital).where(Hospital.id==id)
			)
			return result.scalars().first() 
		
	async def create_new_hospital(self, name: str, address: str, phone: str, rating: float, email: str, city: str) -> Hospital:
		async with self.db_manager.get_session() as session:
			# Проверка на уникальность имени и email
			existing_hospital = await session.execute(
				select(Hospital).filter((Hospital.name == name) | (Hospital.email == email))
			)
			if existing_hospital.scalar():
				raise HTTPException(status_code=400, detail="Hospital with this name or email already exists.")

			# Создание новой записи больницы
			hospital = Hospital(
				name=name,
				address=address,
				phone=phone,
				rating=rating,
				email=email,
				city=city,
			)

			session.add(hospital)
			await session.commit()
			return hospital



	async def create_new_rooms(self, hospital_id: int, rooms: list):
		async with self.db_manager.get_session() as session:
			for room_name in rooms:
				# Проверка на уникальность комнаты
				existing_room = await session.execute(
					select(Room).where(Room.name == room_name, Room.hospital_id == hospital_id)
				)
				existing_room = existing_room.scalar()

				if existing_room:
					raise HTTPException(status_code=400, detail=f"Room '{room_name}' already exists in this hospital.")

				new_room = Room(
					name=room_name,
					hospital_id=hospital_id
				)

				session.add(new_room)

			await session.commit() 
	
	async def delete_hospital(self, id_hospital: int):
		async with self.db_manager.get_session() as session:
			try:
				# Create a delete query
				query = delete(Hospital).where(Hospital.id == id_hospital)
				
				# Execute the delete query
				result = await session.execute(query)
				
				# Commit the changes to persist them in the database
				await session.commit()

				return True 
			except Exception as e:
				
				print(f"Error deleting hospital: {e}")
				return False
	

	async def get_rooms_in_hospital_by_id(self, id_hospital):
		async with self.db_manager.get_session() as session:
			query = select(Room).where(Room.hospital_id==id_hospital)

			result = await session.execute(query)

			return result.scalars().all()


	async def update_hospital_data(self, id: int, update_hospital_data: HospitalSchema):
		async with self.db_manager.get_session() as session:
			async with session.begin():
				# Получаем больницу по ID
				query = select(Hospital).where(Hospital.id == id)
				result = await session.execute(query)
				hospital = result.scalars().first()

				if not hospital:
					raise HTTPException(status_code=404, detail="Hospital not found")

				# Получаем старые данные комнат
				existing_rooms_query = select(Room).where(Room.hospital_id == hospital.id)
				existing_rooms_result = await session.execute(existing_rooms_query)
				existing_rooms = existing_rooms_result.scalars().all()

				# Сохраняем старые данные комнат в список
				old_rooms = [room.name for room in existing_rooms]

				# Обновляем поля больницы
				hospital.name = update_hospital_data.name
				hospital.address = update_hospital_data.address
				hospital.phone = update_hospital_data.phone
				hospital.rating = update_hospital_data.rating
				hospital.email = update_hospital_data.email
				hospital.city = update_hospital_data.city
				
				# Удаляем существующие комнаты
				for room in existing_rooms:
					await session.delete(room)

				# Добавляем новые комнаты из входных данных
				for room_name in update_hospital_data.rooms:
					new_room = Room(name=room_name, hospital_id=hospital.id)
					session.add(new_room)

		return {"is_correct": True, "old_rooms": old_rooms}



	


				



			



	


    
	

