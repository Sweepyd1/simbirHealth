from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
from src.database.database import DatabaseManager
from src.database.Crud import Crud
from config import DATABASE_URL
from src.auth.AuthUtils import AuthUtils
import asyncio
import asyncpg

db = Crud(DatabaseManager(DATABASE_URL))

auth_utils = AuthUtils("HS256", 10, 60, "weffuowewfiiouiowefnuiefnuiowefniowefnio578785478hre", db)

db_start = DatabaseManager(DATABASE_URL)
    
        
