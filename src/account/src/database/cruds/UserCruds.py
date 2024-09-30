from datetime import datetime
from typing import List, Optional
from sqlalchemy.future import select


from ..database import DatabaseManager
from ..models import User


class UsersCRUD:
	db_manager: DatabaseManager



	async def create_user(self, username, firstName,lastName,password):
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
				password = password

			)

			session.add(new_user)
			await session.commit()
			await session.refresh(new_user)
			return new_user


			
	async def get_user_by_username(self, username: str) -> Optional[User]:
		async with self.db_manager.get_session() as session:
			result = await session.execute(select(User).where(User.username == username))
			return result.scalars().first() 

	


    
	

