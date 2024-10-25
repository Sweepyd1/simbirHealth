from ..database import DatabaseManager
from datetime import datetime
from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from ..database import DatabaseManager
from ..models import User
from sqlalchemy import update, delete
from fastapi import HTTPException
class AdminCRUD:
	db_manager: DatabaseManager
	
	async def create_account_by_admin(self,lastName, firstName, username, password, roles):
		async with self.db_manager.get_session() as session:
			new_user = User(
				lastName = lastName, 
				firstName = firstName, 
				username = username, 
				password = password, 
				role = roles

			)
			session.add(new_user)
			await session.commit()
			await session.refresh(new_user)
			return new_user


	async def update_account_by_admin(self, user_id: int, lastName: str, firstName: str, username: str, password: str, roles: str):
		async with self.db_manager.get_session() as session:
			query = select(User).where(User.id == user_id)
			result = await session.execute(query)
			try:
				user = result.scalar_one()
			except NoResultFound:
				raise HTTPException(status_code=404, detail="User not found")

			user.lastName = lastName
			user.firstName = firstName
			user.username = username
			user.password = password 
			user.role = roles

			await session.commit()
			return {"message": "User updated successfully"}

		
	async def get_all_accounts(self, from_, count):
		async with self.db_manager.get_session() as session:
			query = select(User).where(User.id >= from_).limit(count)
			result = await session.execute(query)
			return result.scalars().all()


	async def delete_account_by_admin(self, id: int):
		async with self.db_manager.get_session() as session:
			# Fetch the user before deletion
			user_to_delete = await session.execute(select(User).where(User.id == id))
			user = user_to_delete.scalar_one_or_none()  # Get the User instance

			if user is None:
				raise HTTPException(status_code=404, detail="User not found")

			# Proceed to delete the user
			query = delete(User).where(User.id == id)
			await session.execute(query)
			await session.commit()

			return user 
			

			



  
