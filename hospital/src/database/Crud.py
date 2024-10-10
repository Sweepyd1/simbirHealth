from .database import DatabaseManager
from .cruds.HospitalCruds import HospitalCRUD


class Crud(HospitalCRUD):
    def __init__(self, db_manager: DatabaseManager) -> None:
	    self.db_manager = db_manager