from .database import DatabaseManager
from .cruds.UserCruds import UsersCRUD
from .cruds.AdminCruds import AdminCRUD

class Crud(UsersCRUD, AdminCRUD):
    def __init__(self, db_manager: DatabaseManager) -> None:
	    self.db_manager = db_manager