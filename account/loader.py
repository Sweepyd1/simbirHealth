from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
from src.database.database import DatabaseManager
from src.database.Crud import Crud
from src.database.models import Doctor, User
from config import DATABASE_URL, ALGORITH, ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN_EXPIRE, SECRET_KEY
from src.auth.AuthUtils import AuthUtils
import asyncio
import asyncpg
from sqlalchemy import select, func
from random import choice
db = Crud(DatabaseManager(DATABASE_URL))

auth_utils = AuthUtils(ALGORITH, ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN_EXPIRE, SECRET_KEY, db)

db_start = DatabaseManager(DATABASE_URL)


async def create_doctors():
    async with db_start.get_session() as session:
        result = await session.execute(select(func.count()).select_from(Doctor))
        count = result.scalar()  
        
        if count == 0: 
            specialties = [
                "Хирург", "Кардиолог", "Невролог", "Офтальмолог", 
                "Дерматолог", "Терапевт", "Педиатр", "Стоматолог", 
                "Гинеколог", "Уролог"
            ]
            
            doctors_list = []
            for i in range(1, 101):  # Генерация 100 врачей
                username = f"doctor_{i}"
                password = f"doctor{i}"
                hashed_password = auth_utils.get_password_hash(password)  # Хэшируем пароль
                
                doctor = Doctor(
                    username=username,
                    lastName=f"Фамилия_{i}",
                    firstName=f"Имя_{i}",
                    password=hashed_password,
                    refresh_token="",
                    role=["doctor"],
                    specialty=choice(specialties)  # Случайная специальность
                )
                doctors_list.append(doctor)

            session.add_all(doctors_list)

            # Генерация пользователей
            users_list = [
                User(username="user", lastName="Пользователь", firstName="Обычный", password=auth_utils.get_password_hash("user"), refresh_token="", role=["user"]),
                User(username="admin", lastName="Администратор", firstName="Админ", password=auth_utils.get_password_hash("admin"), refresh_token="", role=["admin"]),
                User(username="manager", lastName="Менеджер", firstName="Менеджер", password=auth_utils.get_password_hash("manager"), refresh_token="", role=["manager"]),
                User(username="doctor", lastName="Доктор", firstName="Врач", password=auth_utils.get_password_hash("doctor"), refresh_token="", role=["doctor"])
            ]

            session.add_all(users_list)
            await session.commit()
        
