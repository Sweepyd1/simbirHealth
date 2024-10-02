from datetime import datetime
from typing import List, Optional
from sqlalchemy.future import select


from ..database import DatabaseManager
from ..models import User


from sqlalchemy import update




class UsersCRUD:
	db_manager: DatabaseManager



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

	


    
	

