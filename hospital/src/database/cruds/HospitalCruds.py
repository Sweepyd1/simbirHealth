from sqlalchemy import func, select, between
from ..database import DatabaseManager


from ..models import Hospital
class HospitalCRUD:
	db_manager: DatabaseManager
	


	async def create_hospital(self):
		async with self.db_manager.get_session() as session:
			result = await session.execute(select(func.count()).select_from(Hospital))
			count = result.scalar() 

			if count == 0:  # Если таблица пуста
				hospitals_list = []

				# Генерация 50 больниц
				for i in range(1, 51):
					hospital = Hospital(
						id=i,
						name=f"Госпиталь №{i}",
						address=f"Улица Примерная, {i}",
						phone=f"+7 (123) 456-78-{90 + i % 10}",  # Примерный телефон
						rating=round(4.0 + (i % 5) * 0.1, 1),  # Генерация рейтинга от 4.0 до 4.9
						email=f"hospital{i}@example.com",
						city="Город " + f"{i}"  # Примерный город
					)
					hospitals_list.append(hospital)

				# Добавляем больницы в сессию
				session.add_all(hospitals_list)
				await session.commit()

	async def get_all_hospital(self, from_: int, count: int):
		async with self.db_manager.get_session() as session:
			# Используем BETWEEN для получения записей с id в диапазоне
			result = await session.execute(
				select(Hospital).where(Hospital.id.between(from_, count))
			)
			return result.scalars().all() 
		

	async def get_hospital_by_id(self, id):
		async with self.db_manager.get_session() as session:
			
			result = await session.execute(
				select(Hospital).where(Hospital.id==id)
			)
			return result.scalars().first() 
		
	async def create_new_hospital(self,id,name,addres,phone,raiting,email,city):
		async with self.db_manager.get_session() as session:

			hospital = Hospital(
							id=id,
							name=name,
							address=addres,
							phone=phone, 
							rating=raiting, 
							email=email,
							city=city 
						)
			
			session.add(hospital)
			await session.commit()

	


    
	

