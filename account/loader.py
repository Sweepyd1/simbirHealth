from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
from src.database.database import DatabaseManager
from src.database.Crud import Crud
from config import DATABASE_URL, ALGORITH, ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN_EXPIRE, SECRET_KEY
from src.auth.AuthUtils import AuthUtils
import asyncio
import asyncpg

db = Crud(DatabaseManager(DATABASE_URL))

auth_utils = AuthUtils(ALGORITH, ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN_EXPIRE, SECRET_KEY, db)

db_start = DatabaseManager(DATABASE_URL)
    
        
