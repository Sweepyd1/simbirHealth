from datetime import datetime
from typing import List, Optional
from sqlalchemy.future import select


from ..database import DatabaseManager
from ..models import User,Doctor


from sqlalchemy import func, update

from sqlalchemy import inspect


class UsersCRUD:
	db_manager: DatabaseManager


	async def create_base_users(self):
		async with self.db_manager.get_session() as session:
			pass
	
	async def create_doctors(self):
		async with self.db_manager.get_session() as session:
			
				result = await session.execute(select(func.count()).select_from(Doctor))
				count = result.scalar()  # Получаем количество записей в таблице

				if count == 0:  # Если таблица пуста
					doctors_list = [
						Doctor(id="1", lastName="Иванов", firstName="Иван", specialty="Терапевт"),
						Doctor(id="2", lastName="Петров", firstName="Петр", specialty="Хирург"),
						Doctor(id="3", lastName="Сидоров", firstName="Сидор", specialty="Кардиолог"),
						Doctor(id="4", lastName="Алексеев", firstName="Алексей", specialty="Невролог"),
						Doctor(id="5", lastName="Мариева", firstName="Мария", specialty="Офтальмолог"),
						Doctor(id="6", lastName="Антонова", firstName="Анна", specialty="Дерматолог"),
						Doctor(id="7", lastName="Еленина", firstName="Елена", specialty="Педиатр"),
						Doctor(id="8", lastName="Дмитриев", firstName="Дмитрий", specialty="Стоматолог"),
						Doctor(id="9", lastName="Ольгина", firstName="Ольга", specialty="Гинеколог"),
						Doctor(id="10", lastName="Викторов", firstName="Виктор", specialty="Уролог"),
						Doctor(id="11", lastName="Натальева", firstName="Наталья", specialty="Эндокринолог"),
						Doctor(id="12", lastName="Кириллов", firstName="Кирилл", specialty="Реабилитолог"),
						Doctor(id="13", lastName="Светлова", firstName="Светлана", specialty="Психиатр"),
						Doctor(id="14", lastName="Андреев", firstName="Андрей", specialty="Аллерголог"),
						Doctor(id="15", lastName="Татьянова", firstName="Татьяна", specialty="Лор")
					]

					# Добавляем докторов в сессию
					session.add_all(doctors_list)

					# Сохраняем изменения в базе данных
					await session.commit()
		





	async def create_user(self, id, username, firstName,lastName,password, refresh_token, role):
		async with self.db_manager.get_session() as session:
			existing_user = await session.execute(select(User).where(User.username == username))
			existing_user = existing_user.scalar()


			if existing_user:
				session.commit()
				return existing_user
			
			new_user = User(
				id=id,
				username=username,
				firstName = firstName,
				lastName = lastName,
				password = password,
				refresh_token = refresh_token,
				role = role

			)

			session.add(new_user)
			await session.commit()
			await session.refresh(new_user)
			return new_user


			
	async def get_user_by_username(self, username: str) -> Optional[User]:
		async with self.db_manager.get_session() as session:
			result = await session.execute(select(User).where(User.username == username))
			return result.scalars().first() 
		

	async def get_user_by_username_and_password(self, username: str, password:str) -> Optional[User]:
		async with self.db_manager.get_session() as session:
			result = await session.execute(
            select(User).where((User.username == username) & (User.password == password))
        )
			return result.scalars().first() 
		


	async def get_user_by_id(self, id: str) -> Optional[User]:
		async with self.db_manager.get_session() as session:
			result = await session.execute(select(User).where(User.id == id))
			return result.scalars().first() 
		
	
		
	async def update_refresh_token(self, id: str, refresh_token: str) -> Optional[User]:
		async with self.db_manager.get_session() as session:
		
			stmt = (
				update(User)
				.where(User.id == id)
				.values(refresh_token=refresh_token)
			)
			
			await session.execute(stmt) 
			await session.commit() 

			
			result = await session.execute(select(User).where(User.id == id))
			return result.scalars().first()
		

	async def update_account_info(self,id, **kwargs):
		async with self.db_manager.get_session() as session:
	

		
			stmt = (
			update(User)
			.where(User.id == id)
			.values(**kwargs)  
			)

			await session.execute(stmt)
			await session.commit()


	async def get_all_doctors_from_db(self):
		async with self.db_manager.get_session() as session:
			result = await session.execute(select(Doctor))
			doctors = result.scalars().all()
			return doctors


		

	


    
	

