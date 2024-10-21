from src.database.database import DatabaseManager
from src.database.Crud import Crud

from config import DATABASE_URL


db = Crud(DatabaseManager(database_url=DATABASE_URL))


db_start = DatabaseManager(DATABASE_URL)