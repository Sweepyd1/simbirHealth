from .database import DatabaseManager
from .cruds.UserCruds import UsersCRUD


class Crud(UsersCRUD):
    def __init__(self, db_manager: DatabaseManager) -> None:
	    self.db_manager = db_manager