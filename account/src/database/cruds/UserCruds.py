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
		

	async def get_user_by_username(self, username: str) -> Optional[User]:
		async with self.db_manager.get_session() as session:
			result = await session.execute(
            select(User).where((User.username == username))
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

		

	


    
	

