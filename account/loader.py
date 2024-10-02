

from src.database.database import DatabaseManager
from src.database.Crud import Crud
from config import DATABASE_URL

import httpx

from src.auth.AuthUtils import AuthUtils




db = Crud(DatabaseManager(DATABASE_URL))

auth_utils = AuthUtils("HS256", 30, 60, "weffuowewfiiouiowefnuiefnuiowefniowefnio578785478hre", db)


