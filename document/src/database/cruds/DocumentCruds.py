from ..database import DatabaseManager
from ..models import History
from ...schemas.schemas import HistorySchemas
from sqlalchemy.future import select
from sqlalchemy.orm import query
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
				doctor_id = data.hospital_id,
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