from datetime import datetime
from typing import List, Optional
from sqlalchemy.future import select
from ..database import DatabaseManager
from ..models import User,Doctor
from sqlalchemy import func, update
from sqlalchemy import inspect
from sqlalchemy.orm import aliased
from sqlalchemy import any_

class UsersCRUD:
	db_manager: DatabaseManager

	async def create_doctors(self):
		async with self.db_manager.get_session() as session:
			result = await session.execute(select(func.count()).select_from(Doctor))
			count = result.scalar()  
			
			if count == 0: 
				doctors_list = [
					Doctor(id=6000, username="petrov_doc", lastName="Петров", firstName="Петр", password="doctor2", refresh_token="", role=["doctor"], specialty="Хирург"),
					Doctor(id=7000, username="sidorov_doc", lastName="Сидоров", firstName="Сидор", password="doctor3", refresh_token="", role=["doctor"], specialty="Кардиолог"),
					Doctor(id=8000, username="alekseev_doc", lastName="Алексеев", firstName="Алексей", password="doctor4", refresh_token="", role=["doctor"], specialty="Невролог"),
					Doctor(id=9000, username="marieva_doc", lastName="Мариева", firstName="Мария", password="doctor5", refresh_token="", role=["doctor"], specialty="Офтальмолог"),
					Doctor(id=10000, username="antonova_doc", lastName="Антонова", firstName="Анна", password="doctor6", refresh_token="", role=["doctor"], specialty="Дерматолог"),
					Doctor(id=5000, username="ivanov_doc", lastName="Иванов", firstName="Иван", password="doctor1", refresh_token="", role=["doctor"], specialty="Терапевт"),
					Doctor(id=1100, username="elenina_doc", lastName="Еленина", firstName="Елена", password="doctor7", refresh_token="", role=["doctor"], specialty="Педиатр"),
					Doctor(id=1200, username="dmitriev_doc", lastName="Дмитриев", firstName="Дмитрий", password="doctor8", refresh_token="", role=["doctor"], specialty="Стоматолог"),
					Doctor(id=1300, username="olgina_doc", lastName="Ольгина", firstName="Ольга", password="doctor9", refresh_token="", role=["doctor"], specialty="Гинеколог"),
					Doctor(id=1400, username="viktorov_doc", lastName="Викторов", firstName="Виктор", password="doctor10" , refresh_token="", role=["doctor"] , specialty="Уролог")
				]
			
				session.add_all(doctors_list)

				users_list = [
					User(id=100076, username="user", lastName="Пользователь", firstName="Обычный", password="user", refresh_token="", role=["user"]),
					User(id=1001, username="admin", lastName="Администратор", firstName="Админ", password="admin", refresh_token="", role=["admin"]),
					User(id=1003, username="manager", lastName="Менеджер", firstName="Менеджер", password="manager", refresh_token="", role=["manager"]),
					User(id=1004, username="doctor", lastName="Доктор", firstName="Врач", password="doctor", refresh_token="", role=["doctor"])
				]

				session.add_all(users_list)
				await session.commit()
			
	async def create_user(self, username, firstName,lastName,password, roles):
		async with self.db_manager.get_session() as session:
			existing_user = await session.execute(select(User).where(User.username == username))
			existing_user = existing_user.scalar()

			if existing_user:
				session.commit()
				return existing_user
			
			new_user = User(
				
				username=username,
				firstName = firstName,
				lastName = lastName,
				password = password,
				role = roles

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
		
	async def get_user_by_id(self, id: int) -> Optional[User]:
		async with self.db_manager.get_session() as session:
			result = await session.execute(select(User).where(User.id == int(id)))
			
			return result.scalars().first() 
		
	async def update_refresh_token(self, id: int, refresh_token: str) -> Optional[User]:
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


	async def get_all_doctors_from_db(self, from_, count):
		async with self.db_manager.get_session() as session:
			DoctorAlias = aliased(Doctor)

			query = (
				select(DoctorAlias)
				.join(User)  # Join with User table
				.where(User.id >= from_, User.role.any("doctor"))
				.limit(count)
        )
			result = await session.execute(query)

		
			
			
			return result.scalars().all()


	async def get_doctor_info_by_id(self, id):
		async with self.db_manager.get_session() as session:
			
			
			DoctorAlias = aliased(Doctor)
			query = (
				select(DoctorAlias)
				.join(User)  # Join with User table
				.where(User.id == id, User.role.any("doctor"))
				
        )

			result = await session.execute(query)
			
			

			return result.scalars().first()

		

	


    
	

