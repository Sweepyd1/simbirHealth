from ..database import DatabaseManager
from ..models import History
from ...schemas.schemas import HistorySchemas
from sqlalchemy.future import select
from sqlalchemy.orm import query
from sqlalchemy import delete



class DocumentCRUD:
	db_manager: DatabaseManager


	async def get_history_for_pacient(self, user_id):
		async with self.db_manager.get_session() as session:
			query = select(History).where(History.pacient_id == user_id)
			result = await session.execute(query)
			result = result.scalars().all()
			return result


	async def get_history_by_id(self,history_id):
		async with self.db_manager.get_session() as session:
			query = select(History).where(History.id == history_id)
			result = await session.execute(query)
			result = result.scalars().all()
			return result
	


    
	

	async def create_history(self,data:History):
		async with self.db_manager.get_session() as session:

			new_history = History(
				date = data.date,
				pacient_id = data.pacient_id,
				hospital_id = data.hospital_id,
				doctor_id = data.doctor_id,
				room = data.room,
				data = data.data


			)
			session.add(new_history)
			await session.commit()
			await session.refresh(new_history)
			return new_history
			


	async def update_history(self, history_id: int, data: History):
		async with self.db_manager.get_session() as session:
			# Получаем существующую запись по ID
			existing_history = await session.execute(
				select(History).where(History.id == history_id)
			)
			existing_history = existing_history.scalar()

			if existing_history is None:
				raise HTTPException(status_code=404, detail="History entry not found.")

			# Обновляем поля записи
			existing_history.date = data.date
			existing_history.pacient_id = data.pacient_id
			existing_history.hospital_id = data.hospital_id
			existing_history.doctor_id = data.doctor_id  # Исправлено с hospital_id на doctor_id
			existing_history.room = data.room
			existing_history.data = data.data

			# Сохраняем изменения в базе данных
			await session.commit()
			await session.refresh(existing_history)

			return existing_history


	async def delete_history_for_hospital(self,hospital_id:int):
		async with self.db_manager.get_session() as session:
			query = delete(History).where(History.hospital_id==hospital_id)
			result = await session.execute(query)
			await session.commit()
			return result.rowcount

	async def delete_all_record_for_doctor(self,doctor_id:int):
		async with self.db_manager.get_session() as session:
			query = delete(History).where(History.doctor_id==doctor_id)
			result = await session.execute(query)
			await session.commit()
			return result.rowcount
	
	async def index_history_records():
		async with database_manager.get_session() as session:
			try:
				# Извлечение всех записей из таблицы History
				result = await session.execute(select(History))
				rows = result.scalars().all()  # Получаем все записи как список объектов History

				# Индексация каждой записи в Elasticsearch
				for row in rows:
					document = row.to_dict()  # Используем метод to_dict для преобразования в словарь
					await es.index(index="history", id=row.id, body=document)
					print(f"Indexed document {row.id}")

			except Exception as e:
				print(f"Error indexing records: {str(e)}")
